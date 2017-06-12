# Implementação para detecção de círculos em Python + OpenCV

Procedimento
-----

**Problema:** Detectar círculos com diâmetro superior a 10 pixels.

**Solução:**
- Aplicação de filtros abertura e fechamento, para eliminar elementos pequenos (ruídos).
- Utilizar a Transformada de Hough para círculos e verificar se o diâmetro dos círculos obtidos é maior que 10 pixels.
- Utilizar a Transformada de Hough para linhas para desconsiderar ítens da solução anterior.
- Repete o processo para diâmetros menores e maiores que 20.
- Ao final do processamento, exibe e salva as imagens processadas.

Imagens de teste na pasta `imagens`.

