// Modelos 3D baixados do Sketchfab.
// Cada entrada aponta para o .glb e para a rotação base que deixa o
// aparelho em pé, com a tela virada para a câmera.
//
// Como o Sketchfab exige login para o Download API oficial (OAuth2) e o
// usuário não conseguia acessar a conta, os modelos foram obtidos via
// dados públicos do viewer (sketchfab-cli) e convertidos para GLB
// (colores/materiais pelo /i/models/{uid}/options + optimize).
//
// O bloco `materiais` mapeia os nomes internos de cada GLB para as partes
// que devem receber a paleta do catálogo (visual.corpo/escuro) e o papel
// de parede gerado em runtime. Assim os modelos originais (vermelho,
// laranja, textura floral etc.) ficam coerentes com o card do aparelho.
//   corpo   -> cor do painel traseiro/estrutura
//   metal   -> aro/estrutura metálica (usa visual.escuro com brilho)
//   escuro  -> detalhes escuros (câmeras, botões, antenas)
//   tela    -> nomes de materiais que recebem o wallpaper
//   telaMalhas -> nomes de malhas (quando o material é compartilhado)
//   ocultar -> nomes de materiais ou malhas que devem ser escondidos

export const modelos3d = {
  // Samsung Galaxy S25 Ultra — Sketchfab: SAMSUNG Galaxy S25 Ultra (Free) por Imagigoo.
  // Licença CC BY 4.0. (O slot usa o S23 Ultra para evitar o uso restrito CC BY-NC-SA.)
  's25-ultra': {
    arquivo: '/modelos/s23-ultra.glb',
    autor: 'Imagigoo',
    link: 'https://sketchfab.com/models/f559464bf0f8453d95a0cd273de3ff0b',
    licenca: 'CC BY 4.0',
    ajuste: {},
    materiais: {
      corpo: ['Rearcase', 'Back_Cover_Glass'],
      metal: ['Bezel', 'Antenna_Plastic'],
      escuro: ['BackCamDeco', 'Cam_Bezel', 'Cam_Body', 'Pen_Body', 'Pen_Top', 'Pen_Button'],
      tela: ['Display_ActiveArea'],
      telaExtra: true, // malha da tela quebrada; usa plano sobreposto
    },
  },
  // Apple iPhone 17 Pro Max — Sketchfab: iPhone 17 Pro Max (Free) por MajdyModels. CC BY 4.0.
  'iphone-17-pro-max': {
    arquivo: '/modelos/iphone-17-pro-max.glb',
    autor: 'MajdyModels',
    link: 'https://sketchfab.com/models/87fc1df741384124a8ce0226d2b2058d',
    licenca: 'CC BY 4.0',
    ajuste: {},
    materiais: {
      corpo: ['backpanel.001', 'basecolor.001'],
      metal: ['metalframe.002', 'metaL.001'],
      escuro: ['gray.001'],
      tela: ['screen.001'],
    },
  },
  // Apple iPhone 17 Pro — Sketchfab: iPhone 17 Pro (Free) por Ranguel. CC BY 4.0.
  'iphone-17-pro': {
    arquivo: '/modelos/iphone-17-pro.glb',
    autor: 'Ranguel',
    link: 'https://sketchfab.com/models/4541aa8a28324b33a2baaf81d263aaec',
    licenca: 'CC BY 4.0',
    ajuste: {},
    materiais: {
      corpo: ['Anodized aluminum', 'Frosted glass'],
      metal: ['Display Frame', 'Metal mesh'],
      escuro: ['Glass tint', 'Plastic antena', 'Plastic port'],
      tela: ['OLED'],
      // `OLED off` é uma segunda tela escura sobreposta e `Glass` é o vidro
      // frontal sem transparência real: os dois causam manchas escuras e
      // z-fighting. A tela `OLED` sozinha já cobre a frente.
      ocultar: ['OLED off', 'Glass'],
      telaExtra: true,
    },
  },
  // Xiaomi 15 Ultra — Sketchfab: (Free) Xiaomi 17 pro max por TahmidTauz. CC BY 4.0.
  'xiaomi-15-ultra': {
    arquivo: '/modelos/xiaomi-15-ultra.glb',
    autor: 'TahmidTauz',
    link: 'https://sketchfab.com/models/014f9880c8764d18b3f4f00aac165a5d',
    licenca: 'CC BY 4.0',
    ajuste: {},
    materiais: {
      corpo: ['Main'],
      escuro: ['Lens'],
      tela: ['Display'],
      ocultar: ['display back'],
    },
  },
  // Google Pixel 9 Pro XL — Sketchfab: Google Pixel 9 & Pixel 9 Pro(Low Poly) por s12311061. CC BY 4.0.
  'pixel-9-pro-xl': {
    arquivo: '/modelos/pixel-9-pro-xl.glb',
    autor: 'LagzDesign',
    link: 'https://sketchfab.com/models/9214c34d4a1b46538f0696492e4ac246',
    licenca: 'CC BY 4.0',
    ajuste: {},
    materiais: {
      corpo: ['BaseFrame'],
      metal: ['RCamFrame'],
      escuro: ['Logo'],
      // O material `Screen` é compartilhado com peças traseiras; por isso a
      // tela é escolhida pelas malhas frontais.
      telaMalhas: ['Base_Screen_0', 'Base_ScreenFrame_0'],
      ocultar: ['RCam1_RCam_0', 'RCam2_RCam_0', 'RCamModule_RCamBack_0', 'FCameraFrame_FCamFrame_0'],
    },
  },
  // Motorola Edge 50 Ultra — Sketchfab: Motorola Edge 50 Neo Grisaille por andras.daradici. CC BY 4.0.
  'edge-50-ultra': {
    arquivo: '/modelos/edge-50-ultra.glb',
    autor: 'andras.daradici',
    link: 'https://sketchfab.com/models/45818636f9194abda61c3fc6d32a6e09',
    licenca: 'CC BY 4.0',
    ajuste: {},
    materiais: {
      corpo: ['Base', 'Leather'],
      escuro: ['Dark Gray'],
      tela: ['Display'],
    },
  },
};

export function modeloDoCelular(id) {
  return modelos3d[id] ?? null;
}
