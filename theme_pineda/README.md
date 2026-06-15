# Pineda — Tema web (Ferretería & Cerrajería)

Tema de sitio web para **Odoo 18** que implementa el design system
**Ferretería y Cerrajería Pineda** (es-CO): estética industrial con rojo
ferretería `#E00010`, amarillo casco `#FFCE00`, tinta `#121212`, contornos negros,
sombras duras con offset, franjas de peligro diagonales y tipografías Saira /
Barlow / Saira Condensed.

## Qué incluye

- **Paleta de marca** (`pineda`), fuentes y botones cuadrados/uppercase aplicados a
  todo el sitio vía `web._assets_primary_variables`
  (`static/src/scss/primary_variables.scss`).
- **Look industrial + estilos del catálogo eCommerce** (`/shop`) vía
  `web.assets_frontend` (`static/src/scss/theme.scss`).
- **Snippets** (bloques editables y arrastrables) en `views/snippets.xml`:
  Hero, Categorías, Entrega y Servicios. Aparecen en el panel **Bloques** del
  editor bajo el grupo **"Pineda"**.
- **Productos con datos reales** (`views/snippets/s_pineda_products.xml`):
  plantilla de tarjeta **"Pineda — Card"** para el snippet dinámico *Productos*
  de `website_sale`. Trae imagen, categoría, precio, stock y "Agregar" desde la
  base de datos. Se usa soltando el bloque **Productos** y eligiendo esa
  plantilla + la categoría deseada (admite carrusel y filtro por categoría).
- **Iconos Lucide** (CDN) inicializados por `static/src/js/lucide_icons.js`.
- Al instalar, `models/theme_pineda.py` selecciona header con buscador, footer de
  enlaces y fija paleta + fuentes.

## Instalación

1. Asegúrate de que `odoo18-custom-addons` esté en el `addons_path`.
2. Activa el modo desarrollador, ve a **Sitio web → Configuración** o **Apps**,
   actualiza la lista de apps e instala **"Pineda — Ferretería & Cerrajería"**
   (depende de `website` y `website_sale`).

## Caveats

- Fuentes (Saira/Barlow) e iconos (Lucide) son **sustituciones** vía Google Fonts /
  CDN; reemplázalos si la marca entrega activos propios.
- Los productos destacados de la homepage son datos de demostración; el catálogo
  real vive en `/shop` (website_sale).
- No se incluyó fotografía de producto: las tarjetas usan iconos de placeholder.
