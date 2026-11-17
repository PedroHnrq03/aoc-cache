# -O2: otimizacao normal de producao.
# -fno-tree-vectorize: impede o gcc de usar SIMD no laco por linha,
#   para comparar apenas o efeito da cache, e nao o de vetorizacao.
CFLAGS = -O2 -fno-tree-vectorize -Wall

percurso: percurso.c
	gcc $(CFLAGS) -o percurso percurso.c

clean:
	rm -f percurso
