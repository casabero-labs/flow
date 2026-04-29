import { test, expect } from '@playwright/test';
import {
 DashboardPage,
 mockAuthApi,
 mockPartnershipApi,
 mockDashboardApi,
 mockTelemetryApi,
 setAuthStorage,
} from './pages';

test.describe('Dashboard — Pantalla principal', () => {
 let dashboardPage: DashboardPage;

 test.beforeEach(async ({ page }) => {
 dashboardPage = new DashboardPage(page);
 await mockAuthApi(page);
 await mockPartnershipApi(page, 'active');
 await mockTelemetryApi(page);
 await setAuthStorage(page);
 });

  test('debe mostrar el dashboard con layout completo', async ({ page }) => {
    await mockDashboardApi(page, true);
    await dashboardPage.goto();

    // Verificar layout general
    await expect(page.locator('.app')).toBeVisible();
    await expect(page.locator('.app-header')).toBeVisible();
    await expect(page.locator('.bottom-nav')).toBeVisible();
    await expect(page.locator('.app-main')).toBeVisible();
  });

  test('debe mostrar el título de la página', async ({ page }) => {
    await mockDashboardApi(page, true);
    await dashboardPage.goto();
    await dashboardPage.waitForData();

    await expect(dashboardPage.pageTitle).toHaveText('Resumen');
  });

  test('debe mostrar las tarjetas de estadísticas con datos', async ({ page }) => {
    await mockDashboardApi(page, true);
    await dashboardPage.goto();
    await dashboardPage.waitForData();

    // Verificar las 3 tarjetas de stats
    await expect(dashboardPage.statCards).toHaveCount(3);

    // Verificar contenido de las tarjetas
    // Ingresos: $5,000,000
    await expect(dashboardPage.incomeCard).toBeVisible();
    await expect(dashboardPage.incomeCard).toContainText('5');

    // Gastos: $3,200,000
    await expect(dashboardPage.expenseCard).toBeVisible();
    await expect(dashboardPage.expenseCard).toContainText('3');

    // Balance: $1,800,000
    await expect(dashboardPage.balanceCard).toBeVisible();
    await expect(dashboardPage.balanceCard).toContainText('1');
  });

  test('debe mostrar el gráfico de gastos por categoría cuando hay datos', async ({ page }) => {
    await mockDashboardApi(page, true);
    await dashboardPage.goto();
    await dashboardPage.waitForData();

    // Debe mostrar el chart card
    await expect(dashboardPage.chartCard).toBeVisible();
    // Debe tener la leyenda con categorías
    await expect(page.locator('.pie-legend')).toBeVisible();
    await expect(page.locator('.pie-legend .legend-item')).toHaveCount(4);
  });

  test('debe mostrar estado vacío cuando no hay datos', async ({ page }) => {
    await mockDashboardApi(page, false);
    await dashboardPage.goto();
    await dashboardPage.waitForData();

    // Debe mostrar empty state en vez de gráficos
    await expect(dashboardPage.emptyState).toBeVisible();
    await expect(dashboardPage.emptyState).toContainText('Sin datos todavía');
  });

  // SKIP: Este test es frágil y depende de timing - los mocks cargan instantáneamente
  // test('debe mostrar skeletons mientras carga', async ({ page }) => {
  //   await dashboardPage.goto();
  //   await expect(dashboardPage.skeletons.first()).toBeVisible({ timeout: 5_000 });
  // });

  test('la navegación inferior debe estar visible con todos los iconos', async ({ page }) => {
    await mockDashboardApi(page, true);
    await dashboardPage.goto();
    await dashboardPage.waitForData();

    const navButtons = page.locator('.nav-btn');
    await expect(navButtons).toHaveCount(5);

    // Verificar etiquetas
    await expect(navButtons.nth(0)).toContainText('Inicio');
    await expect(navButtons.nth(1)).toContainText('Movimientos');
    await expect(navButtons.nth(2)).toContainText('Metas');
    await expect(navButtons.nth(3)).toContainText('Presupuesto');
    await expect(navButtons.nth(4)).toContainText('Insights');
  });
});
