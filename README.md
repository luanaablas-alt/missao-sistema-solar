# Missão Sistema Solar

Jogo educativo de espaço para crianças de 6 a 8 anos: planetas de verdade, leitura e escrita, números e um universo para construir.

## Pastas

- `jogo/` — o jogo completo (`index.html`) e as imagens dos planetas (`tex/`). É aqui que as mudanças são feitas.
- `ferramentas/` — o script que gera o site, o modelo do service worker e os textos da política de privacidade e dos termos de uso.
- `site/` — o que a Vercel publica. É gerado a partir de `jogo/`; não edite `site/index.html` à mão.

## Gerar o site

```
python3 ferramentas/build_site.py
```

## Privacidade (LGPD e ECA Digital)

- Nenhum pedido para outros sites: fontes, biblioteca 3D e imagens são servidas pelo próprio site.
- Sem anúncios, rastreadores, bate-papo ou compras dentro do jogo.
- O progresso fica só no aparelho, separado por criança; a área dos pais (protegida por uma conta de multiplicação) permite ver, baixar e apagar os dados e definir o limite de tempo diário (30 minutos por padrão).
- `site/vercel.json` define as regras de segurança do site (bloqueio de câmera, microfone, localização e de conteúdo de outros endereços).

A política de privacidade e os termos de uso são rascunhos e devem ser revisados por um advogado antes do lançamento.

## Créditos

- Imagens dos planetas: [Solar System Scope](https://www.solarsystemscope.com/textures/), CC BY 4.0, feitas com dados da NASA.
- [three.js](https://threejs.org) r128, licença MIT.
- Fontes Fredoka e Atkinson Hyperlegible, SIL Open Font License (licenças em `site/fonts/`).
