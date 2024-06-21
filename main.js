const { app, BrowserWindow, ipcMain, Menu, shell, clipboard, globalShortcut } = require('electron');
const path = require('path');
const { PythonShell } = require('python-shell');
const fs = require('fs');

let mainWindow;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 700,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false
        },
        title: "Social Media Username Checker by Pedro M.",
        icon: path.join(__dirname, 'icon.png')
    });

    mainWindow.loadFile('splash.html');
}

app.on('ready', () => {
    createWindow();

    const menuTemplate = [
        {
            label: 'Help',
            submenu: [
                {
                    label: 'Contact',
                    click: async () => {
                        await shell.openExternal('https://www.freelancer.com/u/pmesa');
                    }
                }
            ]
        },
        {
            label: 'Donate',
            submenu: [
                {
                    label: 'BTC: bc1qt47jnqke2kqxxd3fvwa6vata2j27atq9hcl0dm',
                    click: () => {
                        clipboard.writeText('bc1qt47jnqke2kqxxd3fvwa6vata2j27atq9hcl0dm');
                    }
                },
                {
                    label: 'ETH: 0xB04165f2523f1cc4889156a0C828F49C87f10FFD',
                    click: () => {
                        clipboard.writeText('0xB04165f2523f1cc4889156a0C828F49C87f10FFD');
                    }
                },
                {
                    label: 'Solana: 7Xv3zsaRdqnRjFB4WXWWViq69dpt2b4aDw3TF2oHKpJ3',
                    click: () => {
                        clipboard.writeText('7Xv3zsaRdqnRjFB4WXWWViq69dpt2b4aDw3TF2oHKpJ3');
                    }
                }
            ]
        }
    ];

    const menu = Menu.buildFromTemplate(menuTemplate);
    Menu.setApplicationMenu(menu);

    globalShortcut.register('F12', () => {
        mainWindow.webContents.toggleDevTools();
    });
});

ipcMain.handle('check-username', async (event, { username }) => {
    return new Promise((resolve, reject) => {
        PythonShell.run('username_checker.py', { args: [JSON.stringify({ username })] }, (err, results) => {
            if (err) {
                reject(err);
            } else {
                resolve(JSON.parse(results[0]));
            }
        });
    });
});

ipcMain.handle('manual-search', async (event, { website, username }) => {
    return new Promise((resolve, reject) => {
        PythonShell.run('username_checker.py', { args: [JSON.stringify({ website, username })] }, (err, results) => {
            if (err) {
                reject(err);
            } else {
                resolve(results);
            }
        });
    });
});

ipcMain.handle('save-results', async (event, { text }) => {
    const filePath = path.join(app.getPath('documents'), 'username_check_results.txt');
    fs.writeFile(filePath, text, (err) => {
        if (err) {
            console.error('Error saving results:', err);
        } else {
            console.log('Results saved successfully to', filePath);
        }
    });
});

ipcMain.handle('clear-results', async (event) => {
    mainWindow.webContents.send('clear-results');
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});