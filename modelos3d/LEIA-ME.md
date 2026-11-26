# Modelos 3D dos celulares

Os modelos ficam em **`public/modelos/`** e são servidos em `/modelos/<nome>.glb`.

## Como baixar no Sketchfab

1. Entre em <https://sketchfab.com> (conta gratuita).
2. Abra o modelo pelo link da tabela.
3. Clique em **Download 3D Model** → escolha **glTF** (ou **glb**).
4. Se vier um `.zip`, extraia e pegue o arquivo `.glb` (ou o `.gltf` + texturas).
5. Salve em `public/modelos/` com o nome exato da coluna **Arquivo**.

Se preferir, jogue os `.zip` em `modelos3d/entrada/` e me avise: eu extraio,
converto e organizo.

## Arquivos esperados

| Celular do site | Arquivo | Modelo sugerido no Sketchfab | Autor | Licença | Faces |
| --- | --- | --- | --- | --- | --- |
| Samsung Galaxy S25 Ultra | `s25-ultra.glb` | [Samsung Galaxy S25 Ultra](https://sketchfab.com/3d-models/samsung-galaxy-s25-ultra-24dc6725f97f4590a6309e9a48129ff2) | mistjs | CC BY | ~12.000 |
| Apple iPhone 17 Pro Max | `iphone-17-pro-max.glb` | [iPhone 17 Pro Max](https://sketchfab.com/models/87fc1df741384124a8ce0226d2b2058d) | MajdyModels | CC BY | 29.562 |
| Apple iPhone 17 Pro | `iphone-17-pro.glb` | [iPhone 17 Pro](https://sketchfab.com/models/4541aa8a28324b33a2baaf81d263aaec) | Ranguel | CC BY | 51.235 |
| Apple iPhone 12 Pro | `iphone-12-pro.glb` | [iPhone 12 Pro](https://sketchfab.com/tags/iphone-12-pro) | Sketchfab | CC BY | ~12.000 |
| Nothing Phone (2) | `nothing-phone-2.glb` | [Nothing Phone (2)](https://sketchfab.com/tags/nothing-phone-2) | Sketchfab | CC BY | ~3.000 |
| OnePlus 12 | `oneplus-12.glb` | [OnePlus 12](https://sketchfab.com/tags/oneplus-12) | Sketchfab | CC BY | ~8.000 |

## Modelos removidos (com defeito / substitutos de baixa qualidade)

- **Xiaomi 15 Ultra** (`xiaomi-15-ultra.glb`): quase vazio, apenas 4 peças, casca fina sem geometria.
- **Google Pixel 9 Pro XL** (`pixel-9-pro-xl.glb`): low-poly com câmera traseira quebrada.
- **Motorola Edge 50 Ultra** (`edge-50-ultra.glb`): na verdade é um Edge 50 Neo com apenas 6 mil faces.

## Alternativa para a Samsung (sem restrição comercial)

O modelo do S25 Ultra é **CC BY-NC-SA** (não permite uso comercial). Se o site
for comercial, use o [Samsung S23 Ultra (Free)](https://sketchfab.com/models/f559464bf0f8453d95a0cd273de3ff0b)
(CC BY, 78.210 faces) e salve como `s25-ultra.glb`.

## Depois de baixar

Avise que os arquivos estão em `public/modelos/`. Eu preencho o manifesto
`src/data/modelos3d.js` com os caminhos e os créditos. Enquanto o `.glb` não
existir, o site usa automaticamente o modelo 3D em CSS (sem quebrar nada).

A licença **CC BY** exige crédito ao autor. O site mostra os créditos na seção
“Dimensões e espessura em 3D”.
