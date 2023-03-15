"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const vscode_1 = require("vscode");
const stripJsonComments = require("strip-json-comments");
const ChildProcess = require("child_process");
const Path = require("path");
const Fs = require("fs");
class TypeScriptCompilerFileWatcher {
    constructor(output, statusChannel, pattern) {
        this.output = output;
        this.statusChannel = statusChannel;
        this.pattern = pattern;
    }
    watch(fn) {
        this.watcher = vscode_1.workspace.createFileSystemWatcher(this.pattern);
        this.watcher.onDidCreate((event) => {
            this.eventType = 'created';
            if (fn)
                fn({ filename: event.fsPath, eventType: this.eventType });
        });
        this.watcher.onDidChange((event) => {
            this.eventType = 'changed';
            if (fn)
                fn({ filename: event.fsPath, eventType: this.eventType });
        });
        this.watcher.onDidDelete((event) => {
            this.eventType = 'deleted';
            if (fn)
                fn({ filename: event.fsPath, eventType: this.eventType });
        });
    }
    dispose() {
        this.watcher.dispose();
    }
}
class TypeScriptCompilerStatusChannel {
    constructor() {
        if (!this.statusItem)
            this.statusItem = vscode_1.window.createStatusBarItem(vscode_1.StatusBarAlignment.Right);
    }
    updateStatus(shortText, longTooltip, color) {
        this.statusItem.tooltip = longTooltip;
        this.statusItem.text = shortText;
        this.statusItem.color = color;
        this.statusItem.show();
    }
    dispose() {
        if (this.statusItem)
            this.statusItem.dispose();
    }
}
class TypeScriptCompilerProjectWatcher extends TypeScriptCompilerFileWatcher {
    constructor(output, statusChannel, tsConfigFile) {
        super(output, statusChannel, new vscode_1.RelativePattern(Path.dirname(tsConfigFile), '**/*.ts'));
        this.tsconfigCompileOnSave = true;
        this.childProcesses = new Map();
        this.configurations = {
            alertOnError: 'alertOnError',
            alertTSConfigChanges: 'alertTSConfigChanges'
        };
        this.tsConfigFile = tsConfigFile;
    }
    watchProject() {
        this.readTsConfigFile();
        this.watch(e => e.filename && this.compile(e.filename));
    }
    reloadTsConfigFile() {
        this.readTsConfigBuildOnSaveOptions();
    }
    readConfiguration(key, defaultValue) {
        // Reading existing configurations for extensions
        var configurationNode = vscode_1.workspace.getConfiguration(`vscode.tsc.compiler`);
        return configurationNode.get(key, defaultValue);
    }
    setConfiguration(key, value) {
        var configurationNode = vscode_1.workspace.getConfiguration(`vscode.tsc.compiler`);
        return configurationNode.update(key, value, vscode_1.ConfigurationTarget.Workspace);
    }
    readTsConfigBuildOnSaveOptions() {
        const contents = Fs.readFileSync(this.tsConfigFile).toString();
        let configs = { compileOnSave: false };
        try {
            const stripedContents = stripJsonComments(contents);
            // while editing a tsconfig.json, parsing JSON for stripedContents can missinterpreted as malformed
            configs = stripedContents && stripedContents.length > 0 ? JSON.parse(stripJsonComments(contents)) : {};
        }
        catch (error) {
            const showError = this.readConfiguration(this.configurations.alertOnError, 'always');
            showError === 'always' ?
                vscode_1.window.showInformationMessage(`Malformed "tsconfig.json" file.`, 'Dismiss', 'Show output', 'Never show again')
                    .then(opted => {
                    if (opted === 'Show output') {
                        this.output.show();
                    }
                    else if (opted === 'Never show again') {
                        this.setConfiguration(this.configurations.alertOnError, 'never');
                    }
                })
                : console.log(`Not showing error informational message`);
            this.output.appendLine('Failed to parse JSON file: ' + this.tsConfigFile + '. Error: ' + error.message);
        }
        if (configs && configs.compileOnSave != null && configs.compileOnSave != undefined) {
            if (configs['include'] instanceof Array) {
                this.pattern = new vscode_1.RelativePattern(Path.dirname(this.tsConfigFile), configs['include'][0]);
            }
            this.tsconfigCompileOnSave = configs.compileOnSave;
        }
    }
    readTsConfigFile() {
        const file = this.tsConfigFile;
        const alertTSConfig = this.readConfiguration(this.configurations.alertTSConfigChanges, 'always');
        const msg = 'Found tsconfig.json file at \'' + file + '\'. File will be used for TypeScript Auto Compile routines.';
        if (alertTSConfig === 'always') {
            vscode_1.window.showInformationMessage(msg, 'Dismiss', 'Never show again')
                .then(opted => {
                if (opted === 'Never show again') {
                    this.setConfiguration(this.configurations.alertTSConfigChanges, 'never');
                }
            });
        }
        this.readTsConfigBuildOnSaveOptions();
    }
    getNodeModulesBinPath(workspaceFolder) {
        return new Promise((resolve) => {
            ChildProcess.exec('npm bin', { cwd: workspaceFolder }, (error, stdout) => {
                if (error)
                    resolve('');
                else
                    resolve(stdout.trim());
            });
        });
    }
    getNodeModules(workspaceFolder) {
        return new Promise((resolve) => {
            ChildProcess.exec('npm list -depth 0 --json', { cwd: workspaceFolder }, (error, stdout) => {
                if (error)
                    resolve(null);
                else
                    resolve(JSON.parse(stdout.trim()));
            });
        });
    }
    findSpecificModule(modules, name) {
        return new Promise((resolve) => {
            if (!modules)
                resolve(false);
            else
                resolve(modules.dependencies != null ? modules.dependencies[name] != null : false);
        });
    }
    testTscPathEnvironment(workspaceDir) {
        return new Promise((resolve) => {
            ChildProcess.exec('tsc --version', { cwd: workspaceDir }, (error) => {
                if (error)
                    resolve(false);
                else
                    resolve(true);
            });
        });
    }
    findNodeModulesByFileParentsFolder(fsFile) {
        var splittedDir = Path.dirname(fsFile).split(Path.sep);
        var candidateFolder = null;
        var i = splittedDir.length;
        while (i > 0) {
            var parentDir = splittedDir.slice(0, i).join(Path.sep);
            parentDir = Path.join(parentDir, `node_modules`);
            if (Fs.existsSync(parentDir)) {
                candidateFolder = parentDir;
                break;
            }
            i--;
        }
        return candidateFolder;
    }
    defineTypescriptCompiler() {
        let binPath;
        // workspace.getWorkspaceFolder is not well implemented for multi-root workspace folders 
        // and workspace.rootPath will be deprecated - changing to file scan aproach
        // https://github.com/Microsoft/vscode/issues/28344
        var wsFolder = vscode_1.workspace.workspaceFolders.filter(folder => folder.uri.fsPath.includes(Path.dirname(this.tsConfigFile))).pop();
        let wsCandidateFolder = wsFolder ? wsFolder.uri.fsPath :
            this.findNodeModulesByFileParentsFolder(this.tsConfigFile) || vscode_1.workspace.rootPath;
        return new Promise((resolve, reject) => {
            if (this.tscPath) {
                resolve(this.tscPath);
            }
            else {
                this.getNodeModulesBinPath(wsCandidateFolder)
                    .then(path => {
                    binPath = path;
                    return this.getNodeModules(wsCandidateFolder);
                })
                    .then(modules => {
                    return this.findSpecificModule(modules, 'typescript');
                })
                    .then(exists => {
                    if (exists) {
                        this.tscPath = `${binPath.split(Path.sep).concat(...[`tsc`]).join(Path.sep)}`;
                        resolve(this.tscPath);
                    }
                    else {
                        return this.testTscPathEnvironment(wsCandidateFolder);
                    }
                })
                    .then(existsEnv => {
                    if (!existsEnv) {
                        reject(`There is no TypeScript compiler available for this workspace. Try to install via npm install typescript command or download it from https://www.typescriptlang.org/index.html#download-links`);
                    }
                    else {
                        this.tscPath = 'tsc';
                        resolve(this.tscPath);
                    }
                });
            }
        });
    }
    compile(fspath) {
        if (!fspath.endsWith('.ts')) {
            return;
        }
        if (!this.tsconfigCompileOnSave) {
            vscode_1.window.setStatusBarMessage(`tsconfig.json (from workspace) turned off 'compile on save' feature.`, 5000);
            this.statusChannel.updateStatus('$(alert) TS [ON]', `TypeScript Auto Compiler can't build on save - see tsconfig.json.`, 'tomato');
            return;
        }
        const filename = Path.basename(fspath);
        const ext = Path.extname(filename).toLowerCase();
        if (ext == '.ts' || filename == 'tsconfig.json') {
            const status = "Auto compiling file \'" + filename + "\'";
            vscode_1.window.setStatusBarMessage(status, 5000);
            this.output.appendLine('');
            this.output.appendLine(status);
            this.statusChannel.updateStatus('$(beaker) TS [ ... ]', `TypeScript Auto Compiler is ON - Compiling changes...`, 'cyan');
            this.defineTypescriptCompiler().then(tsc => {
                console.log(tsc);
                var command = `${tsc} ${fspath}`;
                if (this.tsConfigFile) {
                    command = `${tsc} -p \"${this.tsConfigFile}\"`;
                    this.output.appendLine("Using tsconfig.json at \'" + this.tsConfigFile + "\'");
                }
                if (this.childProcesses.get(filename)) {
                    this.childProcesses.get(filename).kill('SIGHUP');
                }
                this.childProcesses.set(filename, ChildProcess.exec(command, { cwd: vscode_1.workspace.rootPath }, (error, stdout, stderr) => {
                    if (error) {
                        if (error.signal !== 'SIGHUP') {
                            // this.output.show();
                            this.output.appendLine(error.message);
                            this.output.appendLine(stdout.trim().toString());
                            this.output.appendLine('');
                            const showError = this.readConfiguration(this.configurations.alertOnError, 'always');
                            showError === 'always' ?
                                vscode_1.window.showInformationMessage(`Compile errors ocurred while building .ts files.`, 'Dismiss', 'Show output', 'Never show again')
                                    .then(opted => {
                                    if (opted === 'Show output') {
                                        this.output.show();
                                    }
                                    else if (opted === 'Never show again') {
                                        this.setConfiguration(this.configurations.alertOnError, 'never');
                                    }
                                })
                                : console.log(`Not showing error informational message`);
                            this.statusChannel.updateStatus('$(eye) TS [ON]', `TypeScript Auto Compiler is ON - Watching file changes.`, 'white');
                            vscode_1.window.setStatusBarMessage(error.message, 5000);
                        }
                        else {
                            this.output.appendLine('');
                            this.output.appendLine('One compilation was canceled as another process started.');
                        }
                    }
                    else {
                        var successMsg = 'TypeScript Auto Compilation succedded.';
                        this.output.appendLine('');
                        this.output.appendLine(successMsg);
                        this.statusChannel.updateStatus('$(eye) TS [ON]', `TypeScript Auto Compiler is ON - Watching file changes.`, 'white');
                        vscode_1.window.setStatusBarMessage(successMsg, 5000);
                    }
                    this.childProcesses.delete(filename);
                }));
            }).catch(error => {
                this.statusChannel.updateStatus('$(alert) TS [ON]', 'TypeScript Auto Compiler encountered an errror.', 'tomato');
                vscode_1.window.showInformationMessage(error, 'Dismiss');
            });
        }
    }
}
class TypeScriptCompiler {
    constructor() {
        this.watchers = [];
        this.isWatching = false;
    }
    watch() {
        if (!this.isWatching) {
            this.isWatching = true;
            this.output = vscode_1.window.createOutputChannel("TypeScript Auto Compiler");
            this.statusChannel = new TypeScriptCompilerStatusChannel();
            this.output.appendLine('Looking for "tsconfig.json" files..');
            this.output.appendLine('');
            this.watchTsConfigFiles();
            this.watchProjects().then(() => {
                this.statusChannel.updateStatus('$(eye) TS [ON]', 'TypeScript Auto Compiler is ON - Watching file changes.', 'white');
                this.output.appendLine('');
                this.output.appendLine('Watching for file changes..');
            });
        }
    }
    dispose() {
        for (const watcher of this.watchers) {
            watcher.dispose();
        }
        this.watchers = [];
        this.output.dispose();
        this.statusChannel.dispose();
        this.isWatching = false;
    }
    watchTsConfigFiles() {
        for (const workspaceFolder of vscode_1.workspace.workspaceFolders) {
            const pattern = new vscode_1.RelativePattern(workspaceFolder, '**/tsconfig.json');
            const watcher = new TypeScriptCompilerFileWatcher(this.output, this.statusChannel, pattern);
            this.watchers.push(watcher);
            watcher.watch(this.handleTsConfigChange.bind(this));
        }
    }
    handleTsConfigChange(event) {
        this.output.appendLine('');
        switch (event.eventType) {
            case 'created':
                this.setupProjectWatcher(event.filename);
                break;
            case 'deleted':
                this.disposeWatcher(this.findProjectWatcher(event.filename));
                this.output.appendLine('A project "tsconfig.json" file was removed: ' + event.filename);
                break;
            case 'changed':
                const watcher = this.findProjectWatcher(event.filename);
                if (watcher) {
                    watcher.reloadTsConfigFile();
                    this.output.appendLine('A project "tsconfig.json" file was changed: ' + event.filename);
                }
                break;
        }
    }
    watchProjects() {
        return this.findFiles().then(files => {
            for (const file of files) {
                this.setupProjectWatcher(file);
            }
        }).catch(error => {
            this.output.appendLine('Failed to start watchers. Error: ' + error.message + '\n' + error.stack);
        });
    }
    disposeWatcher(watcher) {
        const index = this.watchers.indexOf(watcher);
        if (index !== -1) {
            watcher.dispose();
            this.watchers.splice(index, 1);
        }
    }
    findProjectWatcher(tsConfigFile) {
        for (const watcher of this.watchers) {
            if (watcher instanceof TypeScriptCompilerProjectWatcher && watcher.tsConfigFile === tsConfigFile) {
                return watcher;
            }
        }
        return null;
    }
    setupProjectWatcher(tsConfigFile) {
        const projectCompiler = new TypeScriptCompilerProjectWatcher(this.output, this.statusChannel, tsConfigFile);
        this.output.appendLine('Found "tsconfig.json" file: ' + tsConfigFile);
        this.watchers.push(projectCompiler);
        projectCompiler.watchProject();
    }
    findFiles() {
        return new Promise(resolve => {
            vscode_1.workspace.findFiles('**/tsconfig.json').then(files => {
                resolve(files.map(file => file.fsPath));
            });
        });
    }
}
exports.TypeScriptCompiler = TypeScriptCompiler;
//# sourceMappingURL=TypeScriptCompiler.js.map