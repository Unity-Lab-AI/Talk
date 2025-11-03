import { test, expect } from '@playwright/test';

test.describe('AI Application Deployment Tests', () => {
  const GITHUB_PAGES_URL = 'https://unity-lab-ai.github.io/Talk/';

  test('should load the AI application and attempt to unmute', async ({ page }) => {
    await page.goto(GITHUB_PAGES_URL);

    // Expect the mute indicator button to be visible
    const muteIndicator = page.locator('#mute-indicator');
    await expect(muteIndicator).toBeVisible();
    await expect(muteIndicator).toHaveAttribute('data-state', 'muted');

    // Click the mute indicator to attempt unmuting
    await muteIndicator.click();

    // Expect the state to change to listening, indicating an attempt to unmute/get mic permission
    // This might take a moment for the JS to process and for permissions to be requested.
    // We'll wait for the data-state to change or for a specific console message.
    await expect(muteIndicator).toHaveAttribute('data-state', 'listening', { timeout: 10000 });

    // Optionally, check for console messages related to mic permission
    // page.on('console', msg => {
    //   if (msg.text().includes('Microphone permission denied') || msg.text().includes('Microphone access is required')) {
    //     console.log(`Console: ${msg.text()}`);
    //   }
    // });

    // You might need to add more specific assertions here based on your application's UI changes
    // after attempting to unmute and get microphone permissions.
    // For example, checking for a specific alert or a change in a status message.
  });

  // Add more tests here to cover other main functions of your AI application
  // For example, testing if AI response is received after speaking (if possible in Playwright)
  // or if other UI elements are interactive.
});
