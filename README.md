# Implementação para detecção de círculos em Python + OpenCV

Procedimento
-----

**Problema:** Detectar círculos com diâmetro superior a 10 pixels.

**Solução:**
- Aplicação de filtros abertura e fechamento, para eliminar elementos pequenos (ruídos).
- Utilizar a Transformada de Hough para detectar círculos.
- Utilizar a Transformada de Hough para linhas em cada espaço dos círculos para desconsiderar ítens da solução anterior.
- Repete o processo para diâmetros menores até 12 e maiores que 12.
- Ao final do processamento, exibe e salva as imagens processadas.

Imagens de teste na pasta `imagens`.

