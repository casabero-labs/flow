import { test, expect } from '@playwright/test';
import {
 TransactionsPage,
 mockAuthApi,
 mockPartnershipApi,
 mockTelemetryApi,
 setAuthStorage,
} from './pages';

test.describe('Transactions — Pantalla de movimientos', () => {
 let transactionsPage: TransactionsPage;

 test.beforeEach(async ({ page }) => {
 transactionsPage = new TransactionsPage(page);
 await mockAuthApi(page);
 await mockPartnershipApi(page, 'active');
 await mockTelemetryApi(page);
 await setAuthStorage(page);
 });

  test('debe mostrar la página de movimientos con layout completo', async ({ page }) => {
    await transactionsPage.goto();

    // Verificar layout general (AppLayout)
    await expect(page.locator('.app')).toBeVisible();
    await expect(page.locator('.app-header')).toBeVisible();
    await expect(page.locator('.bottom-nav')).toBeVisible();
    await expect(page.locator('.app-main')).toBeVisible();
  });

  test('debe mostrar título y estado vacío inicial', async ({ page }) => {
    await transactionsPage.goto();

    await expect(transactionsPage.pageTitle).toHaveText('Movimientos');
    await expect(transactionsPage.emptyState).toBeVisible();
    await expect(transactionsPage.emptyState).toContainText('Sin movimientos');
    await expect(transactionsPage.emptyState).toContainText('registrar tu primer ingreso');
  });

  test('debe tener el nav-button de movimientos visible y accesible', async ({ page }) => {
    await transactionsPage.goto();

    // La navegación inferior debe tener un botón de movimientos
    const movimientosBtn = page.locator('.nav-btn').nth(1);
    await expect(movimientosBtn).toBeVisible();
    await expect(movimientosBtn).toContainText('Movimientos');
  });
});
