# Setting Up Your GitHub Repo — Step by Step

## 1. Install prerequisites (if you haven't already)

```bash
# macOS (Homebrew)
brew install git

# Ubuntu / WSL
sudo apt install git

# Verify
git --version
```

Configure your identity (one-time):
```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```

---

## 2. Create a GitHub account & repo

1. Go to [github.com](https://github.com) and sign in.
2. Click the **+** button (top-right) → **New repository**.
3. Name it something like `sum-check-protocol`.
4. Choose **Public** (so others can learn from it).
5. Leave "Initialize with README" **unchecked** (we already have one).
6. Click **Create repository**.
7. Copy the URL shown — it looks like:
   `https://github.com/YOUR_USERNAME/sum-check-protocol.git`

---

## 3. Initialize your local repo and push

Open a terminal and navigate to the project folder:

```bash
cd path/to/sum_check        # wherever you saved the files

git init                    # initialise a new local repo
git add .                   # stage all files
git commit -m "Initial commit: Sum-Check Protocol Manim animation"

# Point local repo at GitHub
git remote add origin https://github.com/YOUR_USERNAME/sum-check-protocol.git

# Push (first time)
git push -u origin main
```

> **Note:** If your default branch is called `master` instead of `main`, run:
> ```bash
> git branch -M main
> ```
> before pushing.

---

## 4. Authenticate with GitHub

GitHub no longer accepts passwords over HTTPS. Use one of:

### Option A — GitHub CLI (easiest)
```bash
# macOS
brew install gh

# Ubuntu
sudo apt install gh

gh auth login    # follow the prompts (browser-based)
```

### Option B — Personal Access Token
1. GitHub → Settings → Developer settings → **Personal access tokens** → Tokens (classic)
2. Generate a token with `repo` scope.
3. When `git push` asks for a password, paste the token.

### Option C — SSH key
```bash
ssh-keygen -t ed25519 -C "you@example.com"
cat ~/.ssh/id_ed25519.pub   # copy this
# Paste it at: GitHub → Settings → SSH and GPG keys → New SSH key

# Then change your remote to SSH:
git remote set-url origin git@github.com:YOUR_USERNAME/sum-check-protocol.git
```

---

## 5. Future updates

Whenever you add or change files:
```bash
git add .
git commit -m "Describe what you changed"
git push
```

---

## 6. Recommended repo additions

- Add rendered `.mp4` clips to a `media/` folder (or upload to YouTube and link in README).
- Add a `LICENSE` file (MIT is common for educational projects).
- Add a GitHub Actions workflow to auto-lint your Python with `flake8`.

---

## Quick reference

| Task | Command |
|---|---|
| See changed files | `git status` |
| See commit history | `git log --oneline` |
| Undo last commit (keep changes) | `git reset HEAD~1` |
| Create a new branch | `git checkout -b feature-name` |
| Push a new branch | `git push -u origin feature-name` |
