import { test, expect } from '@playwright/test';
import { LoginPage, RegisterPage } from './pages';

test.describe('Login — Pantalla de inicio de sesión', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
  });

  test('debe mostrar el formulario de login correctamente', async ({ page }) => {
    await loginPage.goto();

    // Verificar que se renderiza la página de auth
    await expect(page.locator('.auth-page')).toBeVisible();
    await expect(page.locator('.auth-logo')).toHaveText('flow');
    await expect(page.locator('.auth-tagline')).toContainText('finanzas claras');

    // Verificar campos del formulario
    await expect(page.locator('#email')).toBeVisible();
    await expect(page.locator('#password')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toHaveText('Entrar');

    // Verificar link a registro
    await expect(page.locator('a[href="/register"]')).toHaveText('Regístrate');
  });

  test('debe mostrar error con credenciales inválidas', async ({ page }) => {
    await loginPage.goto();

    // Mockear el login para que devuelva error 401
    await page.route('**/api/v1/auth/login', async (route) => {
      await route.fulfill({
        status: 401,
        contentType: 'application/json',
        body: JSON.stringify({ message: 'Credenciales inválidas' }),
      });
    });

    await loginPage.fillEmail('invalido@flow.app');
    await loginPage.fillPassword('wrongpass');
    await loginPage.submit();

    // Verificar mensaje de error
    await expect(loginPage.errorMessage).toBeVisible();
    await expect(loginPage.errorMessage).toContainText('Credenciales inválidas');
  });

  test('debe mostrar error de campo vacío al hacer submit sin datos', async ({ page }) => {
    await loginPage.goto();
    await loginPage.submit();

    // El browser validation debería prevenir el submit
    // Verificar que seguimos en la página de login
    await expect(page).toHaveURL('/login');
  });

  test('debe navegar a registro desde el link', async ({ page }) => {
    await loginPage.goto();
    await loginPage.registerLink.click();
    await expect(page).toHaveURL('/register');
  });
});

test.describe('Register — Pantalla de registro', () => {
  let registerPage: RegisterPage;

  test.beforeEach(async ({ page }) => {
    registerPage = new RegisterPage(page);
  });

  test('debe mostrar el formulario de registro correctamente', async ({ page }) => {
    await registerPage.goto();

    await expect(page.locator('.auth-page')).toBeVisible();
    await expect(page.locator('.auth-logo')).toHaveText('flow');

    // Verificar campos del formulario
    await expect(page.locator('#name')).toBeVisible();
    await expect(page.locator('#email')).toBeVisible();
    await expect(page.locator('#password')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toHaveText('Crear cuenta');

    // Verificar link a login
    await expect(page.locator('a[href="/login"]')).toHaveText('Inicia sesión');
  });

  test('debe mostrar error si la contraseña es muy corta', async ({ page }) => {
    await registerPage.goto();
    await registerPage.fillName('Test User');
    await registerPage.fillEmail('test@flow.app');
    await registerPage.fillPassword('12345'); // menos de 6 caracteres
    await registerPage.submit();

    // El componente Register valida >= 6 caracteres
    await expect(registerPage.errorMessage).toBeVisible();
    await expect(registerPage.errorMessage).toContainText('6 caracteres');
  });

  test('debe navegar a login desde el link', async ({ page }) => {
    await registerPage.goto();
    await registerPage.loginLink.click();
    await expect(page).toHaveURL('/login');
  });
});
