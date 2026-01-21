# Map file extensions to language server commands
LSP_SERVERS = {
    ".py": ["pyright-langserver", "--stdio"],
    ".js": ["typescript-language-server", "--stdio"],
    ".ts": ["typescript-language-server", "--stdio"],
    ".cpp": ["clangd"],
    ".c": ["clangd"],
}