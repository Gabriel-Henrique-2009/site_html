// Modelos 3D baixados do Sketchfab.
// Cada entrada aponta para o .glb e para a rotação base que deixa o
// aparelho em pé, com a tela virada para a câmera.
//
// Os modelos foram obtidos via dados públicos do viewer do Sketchfab e
// convertidos para GLB.
//
// O bloco `materiais` está com todas as listas vazias intencionalmente:
// as cores e texturas originais de cada GLB são mantidas exatamente como
// vieram do Sketchfab, sem pintura da paleta do catálogo por cima.
//   ocultar -> nomes de materiais ou malhas que devem ser escondidos

export const modelos3d = {
  // Samsung Galaxy S25 Ultra — Sketchfab: mistjs. CC BY.
  // GLB atualizado em 26/11/2026. Alguns nomes de material estão em cirílico.
  's25-ultra': {
    arquivo: '/modelos/s25-ultra.glb',
    autor: 'mistjs',
    link: 'https://sketchfab.com/3d-models/samsung-galaxy-s25-ultra-24dc6725f97f4590a6309e9a48129ff2',
    licenca: 'CC BY',
    ajuste: { baseY: 0 },
    materiais: {
      corpo: [],
      metal: [],
      escuro: [],
      tela: [],
      ocultar: [],
    },
  },

  // Apple iPhone 17 Pro Max — Sketchfab: MajdyModels. CC BY 4.0.
  'iphone-17-pro-max': {
    arquivo: '/modelos/iphone-17-pro-max.glb',
    autor: 'MajdyModels',
    link: 'https://sketchfab.com/models/87fc1df741384124a8ce0226d2b2058d',
    licenca: 'CC BY 4.0',
    ajuste: { baseY: 180 },
    materiais: {
      corpo: [],
      metal: [],
      escuro: [],
      tela: [],
    },
  },

  // Apple iPhone 17 Pro — Sketchfab: Ranguel. CC BY 4.0.
  // GLB atualizado em 26/11/2026 (25 MB, versão completa).
  'iphone-17-pro': {
    arquivo: '/modelos/iphone-17-pro.glb',
    autor: 'Ranguel',
    link: 'https://sketchfab.com/models/4541aa8a28324b33a2baaf81d263aaec',
    licenca: 'CC BY 4.0',
    ajuste: { baseY: 180 },
    materiais: {
      corpo: [],
      metal: [],
      escuro: [],
      tela: [],
      ocultar: ['OLED off', 'Glass', 'Frosted glass', 'Glass tint'],
      telaExtra: true,
    },
  },

  // Apple iPhone 12 Pro — Sketchfab. CC BY.
  'iphone-12-pro': {
    arquivo: '/modelos/iphone-12-pro.glb',
    autor: 'Sketchfab',
    link: 'https://sketchfab.com/tags/iphone-12-pro',
    licenca: 'CC BY',
    ajuste: { baseY: 180 },
    materiais: {
      corpo: [],
      metal: [],
      escuro: [],
      tela: [],
      ocultar: [],
    },
  },

  // Nothing Phone (2) — Sketchfab. CC BY.
  'nothing-phone-2': {
    arquivo: '/modelos/nothing-phone-2.glb',
    autor: 'Sketchfab',
    link: 'https://sketchfab.com/tags/nothing-phone-2',
    licenca: 'CC BY',
    ajuste: { baseY: 180 },
    materiais: {
      corpo: [],
      metal: [],
      escuro: [],
      tela: [],
      ocultar: [],
    },
  },

  // OnePlus 12 — Sketchfab. CC BY.
  'oneplus-12': {
    arquivo: '/modelos/oneplus-12.glb',
    autor: 'Sketchfab',
    link: 'https://sketchfab.com/3d-models/oneplus-12-5e2281b99366462188415209beb24dfd',
    licenca: 'CC BY',
    ajuste: { baseY: 180 },
    materiais: {
      corpo: [],
      metal: [],
      escuro: [],
      tela: [],
      ocultar: [],
    },
  },
};

export function modeloDoCelular(id) {
  return modelos3d[id] ?? null;
}
