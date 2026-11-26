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
| Samsung Galaxy S25 Ultra | `s25-ultra.glb` | [SAMSUNG Galaxy S25 Ultra](https://sketchfab.com/models/e3bca75b63c841c0a8aee8733b84a8a9) | zhe_kan | CC BY-NC-SA | 64.636 |
| Apple iPhone 17 Pro Max | `iphone-17-pro-max.glb` | [iPhone 17 Pro Max](https://sketchfab.com/models/87fc1df741384124a8ce0226d2b2058d) | MajdyModels | CC BY | 29.562 |
| Apple iPhone 17 Pro | `iphone-17-pro.glb` | [iPhone 17 Pro](https://sketchfab.com/models/4541aa8a28324b33a2baaf81d263aaec) | Ranguel | CC BY | 51.235 |
| Xiaomi 15 Ultra | `xiaomi-15-ultra.glb` | [(Free) Xiaomi 17 pro max](https://sketchfab.com/models/014f9880c8764d18b3f4f00aac165a5d) _(não existe 15 Ultra)_ | TahmidTauz | CC BY | 36.122 |
| Google Pixel 9 Pro XL | `pixel-9-pro-xl.glb` | [Google Pixel 8 Pro (low-poly)](https://sketchfab.com/models/9214c34d4a1b46538f0696492e4ac246) _(não existe 9 Pro XL)_ | LagzDesign | CC BY | 9.446 |
| Motorola Edge 50 Ultra | `edge-50-ultra.glb` | [Motorola Edge 50 Neo](https://sketchfab.com/models/45818636f9194abda61c3fc6d32a6e09) _(mesma família)_ | andras.daradici | CC BY | 6.110 |

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
