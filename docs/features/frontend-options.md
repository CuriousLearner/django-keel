# Frontend Options

Choose the frontend approach that fits your project.

## Options

### None (API-only)

Pure API backend - perfect for mobile apps or when you have a separate frontend.

### HTMX + Tailwind CSS

Modern, minimal-JavaScript approach with server-rendered HTML.

- **HTMX** for dynamic interactions
- **Tailwind CSS** for styling
- **Alpine.js** for lightweight JavaScript

#### Asset Bundling Options

When you select HTMX + Tailwind, you can choose how assets are delivered:

| Option | Best For | Build Step | External Dependencies |
|--------|----------|------------|----------------------|
| **Vite** (default) | Production apps | Yes | None |
| **CDN** | Prototypes, MVPs | No | Yes (3 CDNs) |

**Vite (Recommended for Production)**

- Bundles Tailwind CSS, HTMX, and Alpine.js locally
- No external CDN dependencies in production
- Proper CSS purging for smaller bundles
- Hot Module Replacement (HMR) in development
- Uses `django-vite` for seamless Django integration

Development:
```bash
docker-compose up  # Starts Django + Vite dev server
```

Production:
- Assets are built during Docker image build
- Served via WhiteNoise from `/static/dist/`

**CDN (Simple, No Build Step)**

- Assets loaded from external CDNs (tailwindcss, unpkg, jsdelivr)
- Zero configuration needed
- Good for quick prototypes
- Not recommended for production (external dependencies)

### Next.js

Full-featured React framework for building modern web applications.

See the [Usage Guide](overview.md) for detailed frontend configuration.
