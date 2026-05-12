import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        'getting-started/installation',
        'getting-started/quick-start',
      ],
    },
    {
      type: 'category',
      label: 'Reference',
      items: [
        'reference/commands',
        'reference/supported-input',
      ],
    },
    {
      type: 'category',
      label: 'Project',
      items: [
        'project/safety',
        'project/status',
        'project/contributing',
      ],
    },
  ],
};

export default sidebars;
