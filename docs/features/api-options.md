# API Options

Django Keel supports multiple API frameworks to suit different project needs.

## Django REST Framework (DRF)

The most popular Django API framework with comprehensive features.

### When to Choose DRF

- Building traditional REST APIs
- Need comprehensive admin integration
- Want built-in authentication and permissions
- Require browsable API for development

### What You Get

- **drf-spectacular** for OpenAPI 3.0 schema generation
- **Swagger UI** for interactive API documentation
- **ReDoc** alternative documentation
- **CORS** configuration for cross-origin requests
- **Pagination**, **filtering**, and **search** configured
- **Versioning** ready to use
- **JWT authentication** integration (optional)

### Example

```python
# apps/api/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        product = self.get_object()
        product.published = True
        product.save()
        return Response({'status': 'published'})
```

Visit `/api/schema/swagger/` for interactive documentation.

## Strawberry GraphQL

Modern, type-safe GraphQL framework with Python 3.12+ support.

### When to Choose GraphQL

- Clients need flexible data queries
- Want strong typing with Python type hints
- Building a single API for multiple clients (web, mobile, etc.)
- Need real-time subscriptions

### What You Get

- **Strawberry** - Modern, Python 3.10+ GraphQL library
- **GraphiQL** interface for development
- **Type-safe** schema with Python type hints
- **Async support** for high performance
- **Django integration** for authentication and permissions
- **Subscriptions** support (with Channels)

### Example

```python
# apps/api/schema.py
import strawberry
from typing import List

@strawberry.type
class Product:
    id: int
    name: str
    price: float

@strawberry.type
class Query:
    @strawberry.field
    def products(self) -> List[Product]:
        return Product.objects.all()

schema = strawberry.Schema(query=Query)
```

Visit `/graphql/` for GraphiQL interface.

## Both DRF + GraphQL

Get the best of both worlds!

### When to Choose Both

- Support both REST and GraphQL clients
- Migrate gradually from REST to GraphQL
- Different endpoints for different use cases
- Maximum flexibility

### Example Structure

```
apps/api/
├── rest/                  # DRF endpoints
│   ├── views.py
│   ├── serializers.py
│   └── urls.py
└── graphql/              # GraphQL schema
    ├── schema.py
    ├── types.py
    └── mutations.py
```

## No API

Choose this for traditional Django views-only projects.

### When to Choose No API

- Building a server-rendered application with Django templates
- Using HTMX for dynamic interactions
- Don't need programmatic API access
- Prefer Django forms and class-based views

## API Authentication

### Django Allauth

- Session-based authentication
- Social authentication (Google, GitHub, etc.)
- Email verification
- Password reset

### JWT (JSON Web Tokens)

- **django-rest-framework-simplejwt**
- Stateless authentication
- Perfect for mobile apps
- Token refresh mechanism

### Both Allauth + JWT

- Session-based for web
- JWT for mobile/API clients
- Flexible authentication options

## CORS Configuration

All API configurations include CORS support:

```python
# config/settings/base.py
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True
```

Configure via environment variables:

```bash
CORS_ALLOWED_ORIGINS=https://frontend.example.com,https://app.example.com
```

## API Versioning

DRF projects are ready for versioning:

```python
# config/settings/base.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
}
```

Use in URLs:

```python
# apps/api/urls.py
urlpatterns = [
    path('v1/', include('apps.api.v1.urls')),
    path('v2/', include('apps.api.v2.urls')),
]
```

## Testing APIs

### DRF Testing

```python
def test_product_list(authenticated_api_client):
    response = authenticated_api_client.get('/api/products/')
    assert response.status_code == 200
    assert len(response.data) > 0
```

### GraphQL Testing

```python
def test_products_query(client):
    query = '''
    query {
        products {
            id
            name
            price
        }
    }
    '''
    response = client.post('/graphql/', {'query': query})
    assert response.status_code == 200
    assert 'data' in response.json()
```

## Performance

### Caching

```python
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ProductViewSet(viewsets.ModelViewSet):
    @method_decorator(cache_page(60 * 15))  # 15 minutes
    @action(detail=False)
    def featured(self, request):
        products = Product.objects.filter(featured=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
```

### Database Optimization

```python
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').prefetch_related('tags')
```

## Next Steps

- [Authentication](authentication.md) - Set up authentication
- [Frontend Options](frontend-options.md) - Connect a frontend
- [Deployment](deployment.md) - Deploy your API
