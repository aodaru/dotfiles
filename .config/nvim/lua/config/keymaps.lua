-- Keymaps are automatically loaded on the VeryLazy event
-- Default keymaps that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/keymaps.lua
-- Add any additional keymaps here
local keymaps = vim.keymap
local opts = { noremap = true, silent = true }

-- Select All
keymaps.set("n", "<C-a>", "gg<S-v><S-g>")

-- Jumplist
keymaps.set("n", "<C-m>", "<C-i>", opts)

--tabs
keymaps.set("n", "te", ":tabedit<Return>", opts)
keymaps.set("n", "<tab>", ":tabnext<Return>", opts)
keymaps.set("n", "<s-tab>", ":tabprev<Return>", opts)

-- Split window
keymaps.set("n", "ss", ":split<Return>", opts)
keymaps.set("n", "sv", ":vsplit<Return>", opts)

-- Move between window
keymaps.set("n", "sh", "<C-w>h")
keymaps.set("n", "sk", "<C-w>k")
keymaps.set("n", "sj", "<C-w>j")
keymaps.set("n", "sl", "<C-w>l")

-- Increment/Decrement dial.vim
keymaps.set("n", "<C-k>", function()
  require("dial.map").manipulate("increment", "normal")
end)
keymaps.set("n", "<C-j>", function()
  require("dial.map").manipulate("decrement", "normal")
end)
