import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'py-sql-cleaner',
  tagline: 'Find, format, and extract SQL embedded in Python files.',
  favicon: 'img/favicon.svg',

  url: 'https://enumura1.github.io',
  baseUrl: '/py-sql-cleaner/',

  organizationName: 'enumura1',
  projectName: 'py-sql-cleaner',

  onBrokenLinks: 'throw',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  stylesheets: [
    {
      href: 'https://fonts.googleapis.com',
      rel: 'preconnect',
    },
    {
      href: 'https://fonts.gstatic.com',
      rel: 'preconnect',
      crossOrigin: 'anonymous',
    },
    {
      href: 'https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap',
      rel: 'stylesheet',
    },
  ],

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/enumura1/py-sql-cleaner/tree/main/website/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/social-card.png',
    navbar: {
      title: 'py-sql-cleaner',
      logo: {
        alt: 'py-sql-cleaner logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          href: 'https://github.com/enumura1/py-sql-cleaner',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'Introduction',
              to: '/docs/intro',
            },
            {
              label: 'Quick Start',
              to: '/docs/getting-started/quick-start',
            },
            {
              label: 'Safety',
              to: '/docs/project/safety',
            },
          ],
        },
        {
          title: 'Project',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/enumura1/py-sql-cleaner',
            },
            {
              label: 'PyPI',
              href: 'https://pypi.org/project/py-sql-cleaner/',
            },
            {
              label: 'Releases',
              href: 'https://github.com/enumura1/py-sql-cleaner/releases',
            },
            {
              label: 'Issues',
              href: 'https://github.com/enumura1/py-sql-cleaner/issues',
            },
          ],
        },
      ],
      copyright: 'Copyright © 2026 enumura1.',
    },
    prism: {
      theme: require('prism-react-renderer').themes.github,
      darkTheme: require('prism-react-renderer').themes.dracula,
      additionalLanguages: ['python', 'sql', 'bash'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
