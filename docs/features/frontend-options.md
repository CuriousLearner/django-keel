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

**Development with Docker (Recommended):**
```bash
docker-compose up  # Starts Django + Vite dev server together
```

**Development without Docker:**
```bash
# Terminal 1: Start Vite dev server
cd frontend
npm install
npm run dev

# Terminal 2: Start Django
python manage.py runserver
```

**Building for Production:**
```bash
# Build optimized assets locally
cd frontend
npm run build  # Outputs to static/dist/

# Or let Docker handle it
docker build -t myapp .  # Multi-stage build includes npm run build
```

**Troubleshooting:**

| Issue | Solution |
|-------|----------|
| Vite HMR not working in Docker | Ensure `VITE_DEV_SERVER_HOST=vite` is set in the Django web service environment |
| Styles not updating | Check Tailwind is scanning `../templates/**/*.html` |
| Assets 404 in production | Run `python manage.py collectstatic` after building |
| `django_vite` template errors | Ensure `DEBUG=False` uses built manifest, not dev server |

**CDN (Simple, No Build Step)**

- Assets loaded from external CDNs (tailwindcss, unpkg, jsdelivr)
- Zero configuration needed
- Good for quick prototypes
- Not recommended for production (external dependencies)

### Next.js

Full-featured React framework for building modern web applications.

See the [Usage Guide](overview.md) for detailed frontend configuration.
