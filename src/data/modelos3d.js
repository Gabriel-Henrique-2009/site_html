// Modelos 3D reais enviados para public/modelos/.
// Cada entrada aponta para o .glb e para a rotação base que deixa o
// aparelho em pé, com a tela virada para a câmera.
export const modelos3d = {
  's25-ultra': {
    arquivo: '/modelos/s23-ultra.glb',
    autor: 'Imagigoo',
    link: 'https://sketchfab.com/models/f559464bf0f8453d95a0cd273de3ff0b',
    licenca: 'CC BY 4.0',
    ajuste: { baseX: 90, baseZ: 180 },
  },
  'iphone-17-pro-max': {
    arquivo: '/modelos/iphone-17-pro-max.glb',
    autor: 'MajdyModels',
    link: 'https://sketchfab.com/models/87fc1df741384124a8ce0226d2b2058d',
    licenca: 'CC BY 4.0',
    ajuste: { baseY: 90 },
  },
  'iphone-17-pro': {
    arquivo: '/modelos/iphone-17-pro-max.glb',
    autor: 'MajdyModels',
    link: 'https://sketchfab.com/models/87fc1df741384124a8ce0226d2b2058d',
    licenca: 'CC BY 4.0',
    ajuste: { baseY: 90 },
  },
  'xiaomi-15-ultra': {
    arquivo: '/modelos/xiaomi-15-ultra.glb',
    autor: 'TahmidTauz',
    link: 'https://sketchfab.com/models/014f9880c8764d18b3f4f00aac165a5d',
    licenca: 'CC BY 4.0',
    ajuste: {},
  },
  'edge-50-ultra': {
    arquivo: '/modelos/edge-50-ultra.glb',
    autor: 'andras.daradici',
    link: 'https://sketchfab.com/models/45818636f9194abda61c3fc6d32a6e09',
    licenca: 'CC BY 4.0',
    ajuste: { baseY: 180 },
  },
};

export function modeloDoCelular(id) {
  return modelos3d[id] ?? null;
}
