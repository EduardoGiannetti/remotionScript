# Remotion video

<p align="center">
  <a href="https://github.com/remotion-dev/logo">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-dark.apng">
      <img alt="Animated Remotion Logo" src="https://github.com/remotion-dev/logo/raw/main/animated-logo-banner-light.gif">
    </picture>
  </a>
</p>

Welcome to your Remotion project!
## Flowchart de funcionamento:
<img width="1498" height="1437" alt="graph" src="https://github.com/user-attachments/assets/e31fa189-346f-4a9c-9f4c-78b59e9258fd" />

## Exemplo de uso:
### JSON da letra criada pelo claude:
<details>
  <summary>Código:</summary>
  
```json
{
    "task_id": "5fc1552d-ebee-4fd3-95fa-44634f358a66",
    "text": [
    "[Intro]",
    "Limpou tudo mesmo, cara é bom",
    "Gosto muito do microondas",
    "[Verse 1]",
    "Se entregar pro et 775 e capaz dele conseguir ler isso aí ainda",
    "Usar máscara cirúrgica pra usar furadeira",
    "Eu recupero tudo ksksksksksk",
    "2 marretadas bem firme bem mais rápido e já era",
    "Formatação física!",
    "Era só mp3 baixados no Kazaa",
    "[Chorus]",
    "Ai depois lembra q tinha uma pasta de bitcoin no HD",
    "Matou 4 bitcoins",
    "Foi ele que vazou o GTA 6",
    "Quando vai ver só histórico do Xvideo",
    "[Verse 2]",
    "Furou até o tijolo da churrasqueira sem necessidade!",
    "Eu uso marreta! Aí não precisa ir na academia nesse dia",
    "Pra qual político vc trabalha?",
    "Polícia tá na bota?",
    "Joga vinagre",
    "Tá devendo.",
    "[Outro]",
    "Que isso seu Jorge, calma ai",
    "Pelo Mor de deus homi"
  ],
    "payload_completo": {
    "audio_duration": 90,
    "batch_size": 1,
    "inference_steps": 20,
    "lyrics": "[Intro]\nLimpou tudo mesmo, cara é bom\nGosto muito do microondas\n\n[Verse 1]\nSe entregar pro et 775 e capaz dele conseguir ler isso aí ainda\nUsar máscara cirúrgica pra usar furadeira\nEu recupero tudo ksksksksksk\n2 marretadas bem firme bem mais rápido e já era\nFormatação física!\nEra só mp3 baixados no Kazaa\n\n[Chorus]\nAi depois lembra q tinha uma pasta de bitcoin no HD\nMatou 4 bitcoins\nFoi ele que vazou o GTA 6\nQuando vai ver só histórico do Xvideo\n\n[Verse 2]\nFurou até o tijolo da churrasqueira sem necessidade!\nEu uso marreta! Aí não precisa ir na academia nesse dia\nPra qual político vc trabalha?\nPolícia tá na bota?\nJoga vinagre\nTá devendo.\n\n[Outro]\nQue isso seu Jorge, calma ai\nPelo Mor de deus homi",
    "model": "acestep-v15-turbo",
    "prompt": "trap ostentação brasileiro, vocal masculino rap confiante com autotune leve, 808 pesado e distorcido, hi-hats rápidos em tercinas, sintetizadores escuros e brilhantes, clima de luxo e marra, produção moderna e limpa",
    "task_type": "text2music",
    "thinking": false,
    "vocal_language": "pt"
  }
}
```

</details>

### JSON dos comentários raspados:
<details>
  <summary>Código:</summary>

```json
{
  "nome": "projeto-exemplo",
  "versao": "1.0.0",
  "ambiente": "producao",
  "recursos": {
    "bancoDeDados": true,
    "cache": false
  },
  "usuarios": [
    "admin",
    "desenvolvedor"
  ]
}
```

</details>

### JSON de saída consumido pelo remotion:
<details>
  <summary>Código:</summary>

```json
{
  "comments": [
    {
      "createdAt": 1783872331,
      "createdAtISO": "2026-07-12T16:05:31.000Z",
      "author": {
        "username": "su.an_san",
        "profilePicUrl": "https://scontent-bog2-1.cdninstagram.com/v/t51.82787-19/669670268_18091123339946350_5121772193865960486_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=106&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=oC_-ea66J0QQ7kNvwHphL3Y&_nc_oc=AdqWe1U2GeJZ88bS0H0CVgeXBCOJv1CIxMEIyc21VJBXrrIDXZZPAOJ-UGG4b3bVkhk&_nc_zt=24&_nc_ht=scontent-bog2-1.cdninstagram.com&_nc_gid=e5tCH3gig-qIpiMj17n4vA&_nc_ss=7da8c&oh=00_AQOKA4s31g_UqA2MyhM8MPCI8ECd8pdJoFIuN78aIsaM2A&oe=6AC0509A"
      },
      "text": "Limpou tudo mesmo, cara é bom",
      "likes": 58,
      "startFrame": 28,
      "durationInFrames": 124
    },
    {
      "createdAt": 1785947645,
      "createdAtISO": "2026-08-05T16:34:05.000Z",
      "author": {
        "username": "gregbispo",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.82787-19/546705011_18526541734048153_5752285641170757947_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=102&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=9ljE2Kjy98IQ7kNvwESyo0x&_nc_oc=AdrXqYAajEQc5WBBUbmn6qdyif-O4P8Q0bOpwkKM4hnFBNgJhtZj72PBz4jFLCmmIGI&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_gid=XfdvofpvxGRWx-rm9c7Ipw&_nc_ss=7da8c&oh=00_AQO8ncRUl-yXDOpfWgz5m0swr2STtJ6P3LaO4Gg1O-s9Sg&oe=6AC067D3"
      },
      "text": "Gosto muito do microondas",
      "likes": 19,
      "startFrame": 155,
      "durationInFrames": 253
    },
    {
      "createdAt": 1785072915,
      "createdAtISO": "2026-07-26T13:35:15.000Z",
      "author": {
        "username": "felip3_duartee",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.82787-19/573576884_18427492495099047_149165562959190876_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=110&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=a0dkXV7MGU8Q7kNvwH-VL0Q&_nc_oc=AdrScNcq6AjwofsrO19Dwc5MRrrhrpGizUmE5dNCUzBeWRxhHkikHXZCi1ggj8EU-ys&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_gid=XfdvofpvxGRWx-rm9c7Ipw&_nc_ss=7da8c&oh=00_AQPficMVuOdZcnYNlu1pYbLNIHbgyxxrs5iEevu_NkUTSQ&oe=6AC0405C"
      },
      "text": "Se entregar pro et 775 e capaz dele conseguir ler isso aí ainda 🤣🤣🤣🤣🤣🤣",
      "likes": 37,
      "startFrame": 408,
      "durationInFrames": 195
    },
    {
      "createdAt": 1784407847,
      "createdAtISO": "2026-07-18T20:50:47.000Z",
      "author": {
        "username": "tiagoelmar",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.82787-19/534327489_18525699568056754_8175858078503738021_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=100&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=xhfIENXhCHoQ7kNvwFtxS6r&_nc_oc=Adoe3zFJVgtZETI-uMd_Y2qkGsYEtualsSIkYYIpTvXqNDiHZR1bNnC9N-du8WuoJtc&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_gid=6XJnT_toSWJ1zY0Ik3iLCw&_nc_ss=73a8c&oh=00_AQNt9Q3WOOh8yg5TYQxt9FM6-wUYLNekNahsSJL3vA224w&oe=6AC063F6"
      },
      "text": "Formatação física!",
      "likes": 11,
      "startFrame": 691,
      "durationInFrames": 83
    },
    {
      "createdAt": 1783879728,
      "createdAtISO": "2026-07-12T18:08:48.000Z",
      "author": {
        "username": "diogo_andrade_007",
        "profilePicUrl": "https://scontent-bog2-1.cdninstagram.com/v/t51.2885-19/240121291_364920978431181_3634310912576765280_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=102&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=caLbTSzWza8Q7kNvwFRCK8g&_nc_oc=AdoDy1gT15QuoPVvYE8MGzzrHlOEQcUOZCRJWAbNA7M7xoIhERyez1t1z8iNPfSTUTY&_nc_zt=24&_nc_ht=scontent-bog2-1.cdninstagram.com&_nc_ss=7da8c&oh=00_AQNboziMqpaD7IfK04j22a8hkN4wgH5V8PKlu28_q_14sA&oe=6AC04180"
      },
      "text": "Era só mp3 baixados no Kazaa",
      "likes": 9,
      "startFrame": 774,
      "durationInFrames": 106
    },
    {
      "createdAt": 1787337054,
      "createdAtISO": "2026-08-21T18:30:54.000Z",
      "author": {
        "username": "leonardocibien",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.82787-19/659174980_18584844493046324_2965504788032705514_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=104&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=uJ5xZ2DeSeAQ7kNvwGCwvmF&_nc_oc=AdqPwPeP8sZ3fkKumtEcdhxDnqpf7PQA38ZuaH5HFoknCHZnmTqjsMGHqNw4UpkSi5s&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_gid=MZlfSiHS14RFURf0wp-X5A&_nc_ss=73a8c&oh=00_AQOoYmJBkcB5RunpwFw5SvRGNjrPGYc-VQjxVysQhjumHA&oe=6AC039D2"
      },
      "text": "Ai depois lembra q tinha uma pasta de bitcoin no HD",
      "likes": 2,
      "startFrame": 880,
      "durationInFrames": 118
    },
    {
      "createdAt": 1784301052,
      "createdAtISO": "2026-07-17T15:10:52.000Z",
      "author": {
        "username": "felipeh_sza",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.2885-19/468410520_1090549852476393_2761623224569896882_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=111&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=ZgfqHCkiFjkQ7kNvwEA4van&_nc_oc=AdoxNmc4Dt53FfD4jm3m8yiAQL-VjMRyTn0kjhc9puCbADjKGgFaNiuoOhvPsJ6DWx4&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_ss=73a8c&oh=00_AQOZmr25eQLhBmu6sQaYPWc1_nqjBQPjzfzWe-CPrryPEg&oe=6AC0338E"
      },
      "text": "Matou 4 bitcoins",
      "likes": 0,
      "startFrame": 998,
      "durationInFrames": 111
    },
    {
      "createdAt": 1788234004,
      "createdAtISO": "2026-09-01T03:40:04.000Z",
      "author": {
        "username": "antonio_eps",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.75761-19/491453395_18456286168074671_6297220016483263731_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=110&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=D8UF4dNO99EQ7kNvwF5ZHd9&_nc_oc=AdqqVPIqhYIccdUiBbuSyfldXsjEh3KSbIkORgubCqP-XkuEm1UixSgkGNWNhbOJr3E&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_gid=az-8OOOiMRGFRWXW2iCPWg&_nc_ss=73a8c&oh=00_AQNzlVdt-CrqNXBcGz8hgw0h1F-FOPIAg0ovIqjhfhXWdg&oe=6AC03537"
      },
      "text": "Foi ele que vazou o GTA 6 😭",
      "likes": 1,
      "startFrame": 1109,
      "durationInFrames": 131
    },
    {
      "createdAt": 1784735426,
      "createdAtISO": "2026-07-22T15:50:26.000Z",
      "author": {
        "username": "marcos_vini_oliver",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.82787-19/799724541_18624667027050676_6239449154310648177_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=104&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=YSlMqSyDWuEQ7kNvwEIPVUY&_nc_oc=AdphLrq3qTnVM1jDBPIm_m1MQ8J1QyGjpaFhFkXuRsY3-SOVgZNx99RbEvOEW6xl6vU&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_gid=6XJnT_toSWJ1zY0Ik3iLCw&_nc_ss=73a8c&oh=00_AQPtUIgUb2t6MFLrneozRcbyvKOG8Vr7gFn1g_f1FlqvKQ&oe=6AC058BC"
      },
      "text": "Quando vai ver só histórico do Xvideo",
      "likes": 0,
      "startFrame": 1255,
      "durationInFrames": 114
    },
    {
      "createdAt": 1784601350,
      "createdAtISO": "2026-07-21T02:35:50.000Z",
      "author": {
        "username": "vinicius.mesquita.pereira",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.2885-19/76847568_454849795430865_5592679299275554816_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=101&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy42NDAuQzMifQ%3D%3D&_nc_ohc=xh4XfKbLfyIQ7kNvwGUrnY5&_nc_oc=AdqHG6HbXZTafZTyFCCvS2fNORu8KwORVpkJkDMUfuTiSNY0AgtoEPge0qKS6A1gtF8&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_ss=73a8c&oh=00_AQNn5ZYOoFge-X3GgiU0h7wiSLBhRizJsxWi54Lr-qu6iA&oe=6AC05220"
      },
      "text": "Furou até o tijolo da churrasqueira sem necessidade! 🤔🫣🤣",
      "likes": 4,
      "startFrame": 1369,
      "durationInFrames": 101
    },
    {
      "createdAt": 1784055196,
      "createdAtISO": "2026-07-14T18:53:16.000Z",
      "author": {
        "username": "talesmaschio",
        "profilePicUrl": "https://scontent-bog2-2.cdninstagram.com/v/t51.2885-19/94426487_536928353654113_2151238274050424832_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=109&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=7gmND1CDZWwQ7kNvwEp5jdF&_nc_oc=AdrkcXdcEpRJ0nHTJms7RjlVP58wUEjABCtNfgMjrmKZmn4cDSrRHAcWCGfI0hOQL8I&_nc_zt=24&_nc_ht=scontent-bog2-2.cdninstagram.com&_nc_ss=7da8c&oh=00_AQOShrayqlZp3rynwqoc-_4I_4626xmIng1fkyypzMAqDg&oe=6AC0564C"
      },
      "text": "Eu uso marreta! Aí não precisa ir na academia nesse dia",
      "likes": 1,
      "startFrame": 1470,
      "durationInFrames": 136
    },
    {
      "createdAt": 1787545772,
      "createdAtISO": "2026-08-24T04:29:32.000Z",
      "author": {
        "username": "alexandre.fc99",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.82787-19/573904966_17849389746591238_2605985535387741063_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=111&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=zBOchx9AO3wQ7kNvwHdKWv3&_nc_oc=AdrAz_ALbBMdCyF9zMlXT3lhKCSmAf1AzHUmjvqbaV2TbxfkNbLVe30Yg3Bfsu9W_LU&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_gid=MZlfSiHS14RFURf0wp-X5A&_nc_ss=73a8c&oh=00_AQNbQZbcvVxOWqEEhO_ML3iYiQE3rwPjZYiaN9dCaoA8_w&oe=6AC0522B"
      },
      "text": "Pra qual político vc trabalha?",
      "likes": 1,
      "startFrame": 1606,
      "durationInFrames": 108
    },
    {
      "createdAt": 1788547104,
      "createdAtISO": "2026-09-04T18:38:24.000Z",
      "author": {
        "username": "marcoscorreia7312",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.2885-19/427301903_917077786814888_5877235021500666222_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=105&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=SxtVJ4fzn_8Q7kNvwF1XyzT&_nc_oc=AdouJhDsJ4C_rMEVXxKFCqhSlBp16Pelp0oiwbaPDu1bhO90EEXHiiGNuCNJU-kscXQ&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_ss=73a8c&oh=00_AQNFk02ye5IyT-uE4KiMcCEn87vSFwcBKZGhC7UdOehyBw&oe=6AC05166"
      },
      "text": "Tá devendo.",
      "likes": 0,
      "startFrame": 1714,
      "durationInFrames": 148
    },
    {
      "createdAt": 1788135882,
      "createdAtISO": "2026-08-31T00:24:42.000Z",
      "author": {
        "username": "1pedrada",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.2885-19/370572708_279610158113329_5363043280853319859_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=108&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy43MTcuQzMifQ%3D%3D&_nc_ohc=X8QhERzvMEAQ7kNvwFcIZYY&_nc_oc=AdouGKBIWzQ97VF4BZ-BteSq3X4mqEhudzLeV6pyTgGh4jGUm_hBpkUW7m0Lxg-RG08&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_ss=73a8c&oh=00_AQNpF2icxLQa2rKFK0iDwuIXmVUd14bO_E6mNblVl0IUUA&oe=6AC06098"
      },
      "text": "Polícia tá na bota?",
      "likes": 1,
      "startFrame": 1862,
      "durationInFrames": 113
    },
    {
      "createdAt": 1788547104,
      "createdAtISO": "2026-09-04T18:38:24.000Z",
      "author": {
        "username": "marcoscorreia7312",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.2885-19/427301903_917077786814888_5877235021500666222_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=105&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDgwLkMzIn0%3D&_nc_ohc=SxtVJ4fzn_8Q7kNvwF1XyzT&_nc_oc=AdouJhDsJ4C_rMEVXxKFCqhSlBp16Pelp0oiwbaPDu1bhO90EEXHiiGNuCNJU-kscXQ&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_ss=73a8c&oh=00_AQNFk02ye5IyT-uE4KiMcCEn87vSFwcBKZGhC7UdOehyBw&oe=6AC05166"
      },
      "text": "Tá devendo.",
      "likes": 0,
      "startFrame": 2076,
      "durationInFrames": 220
    },
    {
      "createdAt": 1784577444,
      "createdAtISO": "2026-07-20T19:57:24.000Z",
      "author": {
        "username": "portuga_proteticocapilar",
        "profilePicUrl": "https://scontent.cdninstagram.com/v/t51.82787-19/707114146_18075209309675224_8517198706492493652_n.jpg?stp=dst-jpg_s150x150_tt6&_nc_cat=103&ccb=7-5&_nc_sid=f7ccc5&efg=eyJ2ZW5jb2RlX3RhZyI6InByb2ZpbGVfcGljLnd3dy4xMDcxLkMzIn0%3D&_nc_ohc=Vtcp2W6B_WEQ7kNvwHm_S74&_nc_oc=Adp_Tid0NDMafOISdlhzoJau0jqpcYp9Qh3nfBsh38REZkz1_FUi_HI4uqHmsoUM11Q&_nc_zt=24&_nc_ht=scontent.cdninstagram.com&_nc_gid=6XJnT_toSWJ1zY0Ik3iLCw&_nc_ss=73a8c&oh=00_AQPSw-0dNvDFEBBy0bXbfd-72RBYtfkgHpI7vtJtOBMT5Q&oe=6AC04282"
      },
      "text": "Pelo Mor de deus homi",
      "likes": 0,
      "startFrame": 2396,
      "durationInFrames": 105
    }
  ],
  "audioPath": "audio/ecf6a66e-e1d6-32e5-f66a-3b668f7096b3.mp3",
  "fps": 30,
  "audioDurationInFrames": 2700
}
```

</details>

### Resultado:
_A ser postado..._

---

## Commands

**Install Dependencies**

```console
npm i
```

**Start Preview**

```console
npm run dev
```

**Render video**

```console
npx remotion render
```

**Upgrade Remotion**

```console
npx remotion upgrade
```


## License

Note that for some entities a company license is needed. [Read the terms here](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md).
