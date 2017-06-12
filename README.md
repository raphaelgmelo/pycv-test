# Implementação para detecção de círculos em Python + OpenCV

Procedimento
-----

**Problema:** detectar círculos com diâmetro superior a 10 pixels.

**Solução:**
- Aplicar filtros abertura e fechamento, para eliminar elementos que confundam-se com círculos.
- Utilizar a Transformada de Hough para círculos e verificar se o diâmetro dos círculos obtidos é maior que 10 pixels.
- Utilizar a Transformada de Hough para linhas para desconsiderar da solução anterior.
- Repete o processo para diâmetros menores e maiores.
- Ao final do processamento, exibe as imagens processadas.

Imagens de teste na pasta `imagens`.

