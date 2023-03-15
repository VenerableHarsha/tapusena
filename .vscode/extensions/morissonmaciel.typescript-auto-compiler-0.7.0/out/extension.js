'use strict';
Object.defineProperty(exports, "__esModule", { value: true });
const TypeScriptCompiler_1 = require("./TypeScriptCompiler");
// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
function activate(context) {
    console.log('Congratulations, your extension "typescript-auto-compiler" is now active!');
    const compiler = new TypeScriptCompiler_1.TypeScriptCompiler();
    compiler.watch();
    // let disposable = commands.registerCommand('extension.sayHello', () => {
    //     window.showInformationMessage('Hello World!');
    // });
    context.subscriptions.push(compiler);
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() {
}
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map