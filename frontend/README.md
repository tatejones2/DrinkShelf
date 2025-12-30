# DrinkShelf Frontend

Modern React/Next.js frontend for the DrinkShelf spirit collector platform.

## Features

- 🔐 User authentication with JWT tokens
- 🍾 Bottle management (create, edit, delete, view)
- 📚 Collections for organizing bottles
- 📝 Tasting notes and reviews
- 🔍 Advanced search and filtering
- 👤 User profiles and flavor analysis
- 🎨 Heritage/Speakeasy themed design

## Tech Stack

- **Framework**: Next.js 16.1 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Authentication**: JWT with js-cookie

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running at http://localhost:8000

### Installation

```bash
npm install
```

### Environment Setup

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home page
│   ├── auth/                   # Authentication pages
│   │   ├── login/page.tsx
│   │   └── register/page.tsx
│   ├── dashboard/page.tsx      # User dashboard
│   ├── search/page.tsx         # Search & discovery
│   └── globals.css
├── components/
│   ├── Navbar.tsx              # Navigation
│   ├── BottleCard.tsx          # Bottle display component
│   └── ClientLayout.tsx        # Client-side wrapper
├── lib/
│   ├── api-client.ts           # Axios instance with interceptors
│   ├── services/               # API service modules
│   │   ├── auth.ts
│   │   ├── bottles.ts
│   │   ├── collections.ts
│   │   └── tasting-notes.ts
│   └── store/
│       └── auth-store.ts       # Zustand state
└── package.json
```

## Pages Implemented

- ✅ `/` - Home page with features
- ✅ `/auth/login` - User login
- ✅ `/auth/register` - User registration
- ✅ `/dashboard` - User dashboard with stats
- ✅ `/search` - Catalog search and filtering

## Coming Next

- 🔜 `/bottles/*` - Bottle detail, creation, editing
- 🔜 `/collections/*` - Collection management
- 🔜 Social features and sharing
- 🔜 Mobile optimization

## Building

```bash
npm run build
npm start
```

## Integration with Backend

The frontend connects to the FastAPI backend (33 routes):
- Authentication (register, login, profiles)
- Bottle management (CRUD, search, filtering)
- Collections (create, manage, sharing)
- Tasting notes (create, aggregate, statistics)
- Advanced search (full-text, filtering, discovery)

## License

Proprietary - DrinkShelf Platform
