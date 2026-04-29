import { Page } from '@playwright/test';

/**
 * Page Object para la pantalla de Login
 */
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async fillEmail(email: string) {
    await this.page.fill('#email', email);
  }

  async fillPassword(password: string) {
    await this.page.fill('#password', password);
  }

  async submit() {
    await this.page.click('button[type="submit"]');
  }

  async login(email: string, password: string) {
    await this.goto();
    await this.fillEmail(email);
    await this.fillPassword(password);
    await this.submit();
  }

  get errorMessage() {
    return this.page.locator('.auth-error');
  }

  get registerLink() {
    return this.page.locator('a[href="/register"]');
  }

  async waitForErrorMessage() {
    await this.errorMessage.waitFor({ state: 'visible', timeout: 10_000 });
  }
}

/**
 * Page Object para la pantalla de Registro
 */
export class RegisterPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/register');
  }

  async fillName(name: string) {
    await this.page.fill('#name', name);
  }

  async fillEmail(email: string) {
    await this.page.fill('#email', email);
  }

  async fillPassword(password: string) {
    await this.page.fill('#password', password);
  }

  async submit() {
    await this.page.click('button[type="submit"]');
  }

  async register(name: string, email: string, password: string) {
    await this.goto();
    await this.fillName(name);
    await this.fillEmail(email);
    await this.fillPassword(password);
    await this.submit();
  }

  get errorMessage() {
    return this.page.locator('.auth-error');
  }

  get loginLink() {
    return this.page.locator('a[href="/login"]');
  }

  async waitForErrorMessage() {
    await this.errorMessage.waitFor({ state: 'visible', timeout: 10_000 });
  }
}

/**
 * Page Object para PartnershipSetup
 */
export class PartnershipSetupPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/setup');
  }

  get createTab() {
    return this.page.locator('button.tab', { hasText: 'Crear invitación' });
  }

  get joinTab() {
    return this.page.locator('button.tab', { hasText: 'Unirse con código' });
  }

  get createInviteButton() {
    return this.page.locator('button.btn-create');
  }

  get joinCodeInput() {
    return this.page.locator('input.code-input');
  }

  get joinSubmitButton() {
    return this.page.locator('button.btn-join');
  }

  get invitationCode() {
    return this.page.locator('.code');
  }

  get errorMessage() {
    return this.page.locator('.setup-error');
  }

  get waitingText() {
    return this.page.locator('.waiting-text');
  }

  /**
   * Simula crear una invitación (mockea la respuesta del API)
   */
  async createInvite() {
    await this.goto();
    await this.createTab.click();
    await this.createInviteButton.click();
  }
}

/**
 * Page Object para el Dashboard
 */
export class DashboardPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/');
  }

  get pageTitle() {
    return this.page.locator('.page-title');
  }

  get statCards() {
    return this.page.locator('.stat-card');
  }

  get incomeCard() {
    return this.page.locator('.stat-card .stat-value.income');
  }

  get expenseCard() {
    return this.page.locator('.stat-card .stat-value.expense');
  }

  get balanceCard() {
    return this.page.locator('.stat-card .stat-value.balance');
  }

  get skeletons() {
    return this.page.locator('.skeleton');
  }

  get emptyState() {
    return this.page.locator('.empty-state');
  }

  get chartCard() {
    return this.page.locator('.chart-card');
  }

  async waitForData() {
    // Espera a que los skeletons desaparezcan (datos cargados)
    await this.skeletons.first().waitFor({ state: 'hidden', timeout: 15_000 }).catch(() => {});
  }
}

/**
 * Page Object para Transactions
 */
export class TransactionsPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/transactions');
  }

  get pageTitle() {
    return this.page.locator('.page-title');
  }

  get emptyState() {
    return this.page.locator('.empty-state');
  }
}

/**
 * Helper para mockear el API de autenticación
 */
export async function mockAuthApi(page: Page) {
  // Mock login endpoint
  await page.route('**/api/auth/login', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        token: 'mock-token-e2e-test',
        user: { id: '1', email: 'test@flow.app', name: 'Test User' },
      }),
    });
  });

  // Mock register endpoint
  await page.route('**/api/auth/register', async (route) => {
    await route.fulfill({
      status: 201,
      contentType: 'application/json',
      body: JSON.stringify({
        token: 'mock-token-e2e-test',
        user: { id: '2', email: 'newuser@flow.app', name: 'New User' },
      }),
    });
  });

  // Mock get /auth/me
  await page.route('**/api/auth/me', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        id: '1',
        email: 'test@flow.app',
        name: 'Test User',
      }),
    });
  });
}

/**
 * Helper para mockear partnership status
 */
export async function mockPartnershipApi(page: Page, status: 'none' | 'active' | 'pending' = 'none') {
  await page.route('**/api/partnerships/status', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        status,
        ...(status === 'active' ? {
          partner: { id: 'partner-1', name: 'Partner', email: 'partner@flow.app' },
          joinedAt: new Date().toISOString(),
        } : {}),
      }),
    });
  });

  // Mock create invite
  await page.route('**/api/partnerships/invite', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({
        code: 'ABCDEF',
        expiresAt: new Date(Date.now() + 86400000).toISOString(),
      }),
    });
  });

 // Mock join with code
 await page.route('**/api/partnerships/join', async (route) => {
   // Devuelve 400 para códigos inválidos
   const body = route.request().postData();
   const isInvalid = body && (body.includes('ABC') || body.includes('ZZZZZZ'));
   
   if (isInvalid) {
     await route.fulfill({
       status: 400,
       contentType: 'application/json',
       body: JSON.stringify({ message: 'Código de invitación inválido' }),
     });
   } else {
     await route.fulfill({
       status: 200,
       contentType: 'application/json',
       body: JSON.stringify({
         status: 'active',
         partner: { id: 'partner-1', name: 'Partner', email: 'partner@flow.app' },
         joinedAt: new Date().toISOString(),
       }),
     });
   }
 });
}

/**
 * Helper para mockear el Dashboard API
 */
export async function mockDashboardApi(page: Page, hasData = true) {
  const dashboardData = hasData
    ? {
        income_this_month: 5000000,
        expense_this_month: 3200000,
        balance_this_month: 1800000,
        category_totals: [
          { category: 'Alimentación', total: 1200000, percentage: 37.5, icon: '🍕' },
          { category: 'Transporte', total: 600000, percentage: 18.75, icon: '🚗' },
          { category: 'Servicios', total: 800000, percentage: 25.0, icon: '🏠' },
          { category: 'Ocio', total: 600000, percentage: 18.75, icon: '🎬' },
        ],
        monthly_trend: [
          { month: 'Ene', income: 4500000, expense: 3000000 },
          { month: 'Feb', income: 4800000, expense: 3100000 },
          { month: 'Mar', income: 5000000, expense: 3200000 },
        ],
      }
    : {
        income_this_month: 0,
        expense_this_month: 0,
        balance_this_month: 0,
        category_totals: [],
        monthly_trend: [],
      };

  await page.route('**/api/dashboard', async (route) => {
    console.log('DASHBOARD MOCK:', JSON.stringify(dashboardData).slice(0, 100));
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(dashboardData),
    });
  });
}

/**
 * Helper para autenticar al usuario en el storage del navegador
 */
export async function setAuthStorage(page: Page) {
  // Navigate to the app first — localStorage is blocked on about:blank
  await page.goto('/');
  await page.evaluate(() => {
    localStorage.setItem('flow_token', 'mock-token-e2e-test');
    localStorage.setItem('flow_user', JSON.stringify({
      id: '1',
 email: 'test@flow.app',
 name: 'Test User',
 }));
 });
}

/**
 * Helper para mockear el endpoint de telemetry — se llama al cargar la app
 * y causa errores si no hay backend.
 */
export async function mockTelemetryApi(page: Page) {
  await page.route('**/api/telemetry/**', async (route) => {
    await route.fulfill({
      status: 201,
      contentType: 'application/json',
      body: JSON.stringify({}),
    });
  });
}
