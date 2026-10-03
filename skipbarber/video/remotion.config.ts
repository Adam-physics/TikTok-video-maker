import {Config} from '@remotion/cli/config';

// The cloud container cannot download Remotion's own Chrome, so use the preinstalled one.
const shell = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
import fs from 'fs';
if (fs.existsSync(shell)) Config.setBrowserExecutable(shell);
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(95);
Config.setConcurrency(4);
