# NexERP - Enterprise Resource Planning System

**Production-ready, industrial-grade ERP with real-time collaboration**

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Launch with Docker

```bash
# Clone the repository
git clone <your-repo-url>
cd erp

# Start all services
docker-compose up --build

# Access applications
Frontend: http://localhost:3000
Backend API: http://localhost:8000/docs
Database: localhost:5432
```

### First Time Setup

1. **Sign Up**: Navigate to `http://localhost:3000/auth/signup`
2. **Create Workspace**: During signup, you'll automatically create your workspace
3. **Explore**: Use the sidebar to navigate through all modules

## 📦 Features

- **Manufacturing**: BOM, Production Orders (SPK), Work-in-Progress tracking
- **Procurement**: Purchase Orders, Goods Receipt Notes, Supplier management
- **Sales & Distribution**: Sales Orders, Delivery Orders, Customer invoicing
- **Inventory**: Multi-warehouse, FIFO/Average costing, Stock ledger
- **Finance & Accounting**: Auto-journaling, General Ledger, Cash & Bank
- **HR**: Employee management, Department structure
- **Analytics**: Real-time KPIs, Sales trends, Top products
- **Collaboration**: Notifications, Approval workflows, Real-time alerts
- **Import/Export**: Bulk Excel operations for all modules

## 🛠️ Development

### Backend (FastAPI)

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest
```

### Frontend (Next.js)

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests (if implemented)
cd frontend
npm test
```

## 🚢 Production Deployment

### Environment Variables

Copy `.env.example` to `.env` and update:

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with production values
```

**Critical variables to update:**

- `SECRET_KEY`: Generate a strong random key
- `DATABASE_URL`: Production database connection
- `FRONTEND_URL`: Your production domain

### Database Migration

```bash
# If using Alembic (recommended for production)
cd backend
alembic upgrade head
```

### Deploy to Cloud

**Docker-based deployment (AWS ECS, Google Cloud Run, Azure Container Instances):**

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Push to registry
docker tag nexerp-backend <your-registry>/nexerp-backend:latest
docker push <your-registry>/nexerp-backend:latest

docker tag nexerp-frontend <your-registry>/nexerp-frontend:latest
docker push <your-registry>/nexerp-frontend:latest
```

## 📊 Architecture

```
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Configuration, security, dependencies
│   │   ├── models/       # SQLAlchemy models
│   │   ├── services/     # Business logic
│   │   └── main.py       # Application entry point
│   ├── tests/            # Pytest test suite
│   └── requirements.txt
│
├── frontend/             # Next.js application
│   ├── src/
│   │   ├── app/         # App Router pages
│   │   ├── components/  # React components
│   │   ├── lib/         # Utilities
│   │   └── store/       # Zustand state management
│   └── package.json
│
└── docker-compose.yml   # Development orchestration
```

## 🔐 Security

- **JWT Authentication**: Token-based auth with refresh capability
- **Password Hashing**: Bcrypt with salt rounds
- **RBAC**: Role-based access control (foundation implemented)
- **SQL Injection Protection**: SQLAlchemy ORM parameterization
- **CORS**: Configurable cross-origin policies

## 📝 API Documentation

Once running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - See LICENSE file for details

## 💬 Support

For issues and questions:

- GitHub Issues: [Your repo issues URL]
- Email: <support@nexerp.com>

---

**Built with ❤️ using FastAPI, Next.js, and PostgreSQL**
