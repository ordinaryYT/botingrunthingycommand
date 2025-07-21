require('dotenv').config();
const { Client, GatewayIntentBits } = require('discord.js');
const puppeteer = require('puppeteer');

const client = new Client({ intents: [GatewayIntentBits.Guilds, GatewayIntentBits.GuildMessages, GatewayIntentBits.MessageContent] });

client.once('ready', () => {
  console.log(`Logged in as ${client.user.tag}`);
});

client.on('messageCreate', async message => {
  if (message.author.bot) return;

  if (message.content.toLowerCase() === '!floss') {
    await message.channel.send('Starting task, please wait...');

    try {
      const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
      });
      const page = await browser.newPage();

      await page.goto('https://app.fnlb.net/bot/67fad93a739ee0f4991bb53c', { waitUntil: 'networkidle2' });

      // Wait for chat input selector (you need to replace this with actual selector)
      const chatSelector = 'textarea'; // Assuming a textarea, adjust if different

      await page.waitForSelector(chatSelector);

      // Click chat input
      await page.click(chatSelector);

      // Type "floss" and press Enter
      await page.type(chatSelector, 'floss');
      await page.keyboard.press('Enter');

      await browser.close();

      await message.channel.send('Task completed: typed "floss" in chat!');
    } catch (error) {
      console.error('Error during Puppeteer task:', error);
      await message.channel.send('Oops, something went wrong while running the task.');
    }
  }
});

client.login(process.env.DISCORD_BOT_TOKEN);
