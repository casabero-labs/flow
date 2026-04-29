import { test, expect } from '@playwright/test';
import {
 RegisterPage,
 LoginPage,
 PartnershipSetupPage,
 mockAuthApi,
 mockPartnershipApi,
 mockTelemetryApi,
 setAuthStorage,
} from './pages';

test.describe('PartnershipSetup — Configuración de pareja', () => {
 let setupPage: PartnershipSetupPage;

 test.beforeEach(async ({ page }) => {
 setupPage = new PartnershipSetupPage(page);
 await mockAuthApi(page);
 await mockTelemetryApi(page);
 await setAuthStorage(page);
 });

  test('debe mostrar la pantalla de setup correctamente', async ({ page }) => {
    await mockPartnershipApi(page, 'none');
    await setupPage.goto();

    await expect(page.locator('.setup-page')).toBeVisible();
    await expect(page.locator('.setup-title')).toHaveText('Conectar con tu pareja');
    await expect(setupPage.createTab).toBeVisible();
    await expect(setupPage.joinTab).toBeVisible();
  });

  test('debe mostrar la opción de crear invitación por defecto', async ({ page }) => {
    await mockPartnershipApi(page, 'none');
    await setupPage.goto();

    // Por defecto debe estar en modo 'create'
    await expect(setupPage.createTab).toHaveClass(/active/);
    await expect(setupPage.createInviteButton).toBeVisible();
    await expect(setupPage.createInviteButton).toHaveText('Generar código');
  });

  test('debe generar un código de invitación al hacer clic en "Generar código"', async ({ page }) => {
    await mockPartnershipApi(page, 'none');
    await setupPage.goto();

    await setupPage.createInviteButton.click();

    // Debe mostrar el código generado
    await expect(setupPage.invitationCode).toBeVisible();
    await expect(setupPage.invitationCode).toHaveText('ABCDEF');
    await expect(setupPage.waitingText).toContainText('Esperando');
  });

  test('debe permitir cambiar al modo "Unirse con código"', async ({ page }) => {
    await mockPartnershipApi(page, 'none');
    await setupPage.goto();

    await setupPage.joinTab.click();
    await expect(setupPage.joinTab).toHaveClass(/active/);
    await expect(setupPage.joinCodeInput).toBeVisible();
    await expect(setupPage.joinSubmitButton).toHaveText('Unirse');
  });

  test('debe mostrar error si el código de unión es inválido', async ({ page }) => {
    await mockPartnershipApi(page, 'none');
    await setupPage.goto();

    await setupPage.joinTab.click();

  // Ingresar código de menos de 6 caracteres
  await setupPage.joinCodeInput.fill('ABC');

  // El botón debería estar disabled si el código no tiene 6 caracteres
  await expect(setupPage.joinSubmitButton).toBeDisabled();

  // Ingresar código de 6 caracteres pero inválido
  await setupPage.joinCodeInput.fill('ZZZZZZ');
  await setupPage.joinSubmitButton.click();

    await expect(setupPage.errorMessage).toBeVisible();
  });

  test('debe redirigir al dashboard si la partnership ya está activa', async ({ page }) => {
    await mockPartnershipApi(page, 'active');
    await setupPage.goto();

    // Debería redirigir al dashboard
    await expect(page).toHaveURL('/', { timeout: 10_000 });
  });
});

test.describe('Flujo completo: Register → Setup → Login → Dashboard', () => {
  test('registro exitoso redirige a /setup', async ({ page }) => {
    const registerPage = new RegisterPage(page);
    await mockAuthApi(page);

    await registerPage.register('Nuevo Usuario', 'nuevo@flow.app', 'password123');

    // Después de register exitoso, redirige a /setup
    await expect(page).toHaveURL('/setup', { timeout: 10_000 });
  });

  test('login exitoso con partnership activa redirige a dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await mockAuthApi(page);
    await mockPartnershipApi(page, 'active');

    await loginPage.login('test@flow.app', 'password123');

    // Debe redirigir a dashboard
    await expect(page).toHaveURL('/', { timeout: 10_000 });
  });

  test('login exitoso sin partnership redirige a /setup', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await mockAuthApi(page);
    await mockPartnershipApi(page, 'none');

    await loginPage.login('test@flow.app', 'password123');

    // Debe redirigir a setup
    await expect(page).toHaveURL('/setup', { timeout: 10_000 });
  });
});
