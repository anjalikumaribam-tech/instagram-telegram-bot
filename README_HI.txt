SETUP — Dhyan se padhein

Yeh Netlify webhook starter hai. Sirf upload karne se bot automatic start nahi hota.
1. Netlify par project deploy karein.
2. Site settings / Environment variables mein BOT_TOKEN naam ka variable banayein aur BotFather token value mein daalein.
3. Site ko redeploy karein.
4. Browser mein yeh URL kholein, BOT_TOKEN aur SITE_NAME ko apne values se replace karein:
https://api.telegram.org/botBOT_TOKEN/setWebhook?url=https://SITE_NAME.netlify.app/telegram-webhook
5. Telegram bot par /start bhejein, phir public Instagram Reel link bhejein.

LIMITATIONS:
- Instagram extraction unreliable ho sakta hai; private posts ya access restrictions bypass nahi hoti.
- Netlify function + Telegram URL fetching ke saath kuch links fail kar sakte hain.
- Token ko public code, screenshot, ya chat mein share na karein. Leak ho to @BotFather se revoke karein.
