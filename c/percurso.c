/*
 * percurso.c — Impacto da memoria cache no desempenho de software
 * Percorre uma matriz N x N por LINHA e por COLUNA e mede o tempo.
 *
 * Uso:   ./percurso N REPETICOES
 * Saida: uma linha CSV  ->  N,tempo_linha_ms,tempo_coluna_ms,razao
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/* Tempo atual em milissegundos (relogio monotonico, nao sofre ajuste de hora) */
static double agora_ms(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec * 1e3 + t.tv_nsec / 1e6;
}

/* ===== NUCLEO DO EXPERIMENTO ===== */

/* Por LINHA: o indice j (coluna) varia no laco de dentro.
 * Elementos vizinhos na memoria sao lidos em sequencia -> localidade espacial. */
long long soma_por_linha(const int *m, int n) {
    long long soma = 0;
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            soma += m[i * n + j];          /* equivale a m[i][j] */
    return soma;
}

/* Por COLUNA: o indice i (linha) varia no laco de dentro.
 * Cada acesso salta n*4 bytes -> quase nenhuma localidade espacial. */
long long soma_por_coluna(const int *m, int n) {
    long long soma = 0;
    for (int j = 0; j < n; j++)
        for (int i = 0; i < n; i++)
            soma += m[i * n + j];          /* equivale a m[i][j] */
    return soma;
}

/* ================================== */

static int cmp_double(const void *a, const void *b) {
    double x = *(const double *)a, y = *(const double *)b;
    return (x > y) - (x < y);
}

/* Mediana: menos sensivel a interferencias do sistema operacional que a media */
static double mediana(double *v, int k) {
    qsort(v, k, sizeof(double), cmp_double);
    return (k % 2) ? v[k / 2] : (v[k / 2 - 1] + v[k / 2]) / 2.0;
}

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "uso: %s N REPETICOES\n", argv[0]);
        return 1;
    }
    int n   = atoi(argv[1]);
    int rep = atoi(argv[2]);

    /* Matriz contigua em memoria, ordem row-major (igual a int m[n][n]) */
    int *m = malloc((size_t)n * n * sizeof(int));
    if (!m) { fprintf(stderr, "sem memoria\n"); return 1; }
    for (long k = 0; k < (long)n * n; k++) m[k] = (int)(k % 100);

    double *tl = malloc(rep * sizeof(double));
    double *tc = malloc(rep * sizeof(double));
    long long s1 = 0, s2 = 0;

    for (int r = 0; r < rep; r++) {
        double t0 = agora_ms();
        s1 = soma_por_linha(m, n);
        double t1 = agora_ms();
        s2 = soma_por_coluna(m, n);
        double t2 = agora_ms();
        tl[r] = t1 - t0;
        tc[r] = t2 - t1;
    }

    /* As duas somas tem de ser iguais: mesmo trabalho, ordem diferente */
    if (s1 != s2) { fprintf(stderr, "ERRO: somas diferentes!\n"); return 2; }

    double ml = mediana(tl, rep), mc = mediana(tc, rep);
    printf("%d,%.4f,%.4f,%.2f\n", n, ml, mc, mc / ml);

    free(m); free(tl); free(tc);
    return 0;
}
