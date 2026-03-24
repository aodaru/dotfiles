return {
  -- Emmet plugin for LSP integration
  {
    "olrtg/nvim-emmet",
    dependencies = {
      "neovim/nvim-lspconfig",
    },
  },

  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        emmet_ls = {
          filetypes = {
            "html",
            "json",
            "css",
            "markdown",
            "javascriptreact",
            "typescriptreact",
            "blade",
          },
          -- Other Emmet options can be configured here
        },
        cssls = {
          filetype = {
            "css",
            "scss",
          },
        },
      },
    },
  },
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    config = function()
      -- Custom filetype detection for .blade.php files.
      vim.filetype.add({
        pattern = {
          [".*%.blade%.php"] = "blade",
        },
      })

      -- NOTE: This is a simplified, explicit configuration.
      -- The previous method of extending 'opts' was causing load order issues.
      -- You may need to add other language parsers to the 'ensure_installed' list
      -- if they were provided by your base Neovim configuration.
      require("nvim-treesitter").setup({
        ensure_installed = {
          "blade",
          "php_only",
          "lua",
          "vim",
          "vimdoc",
          "javascript",
          "html",
          "css",
        },
        auto_install = true,
        highlight = { enable = true },
        indent = { enable = true },
        parser_config = {
          blade = {
            install_info = {
              url = "https://github.com/EmranMR/tree-sitter-blade",
              files = { "src/parser.c" },
              branch = "main",
            },
            filetype = "blade",
          },
        },
      })
    end,
  },
  {
    "saghen/blink.cmp",
    opts = {
      keymap = {
        preset = "default",
        ["<Tab>"] = { "select_next", "fallback" },
        ["<S-Tab>"] = { "select_prev", "fallback" },
        ["<C-Space>"] = { "accept", "fallback" },
      },
    },
  },
  {
    "mason-org/mason.nvim",
    opts = {
      ensure_installed = {
        "stylua",
        "emmet-language-server",
      },
    },
  },
}
