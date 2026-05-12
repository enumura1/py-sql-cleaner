import clsx from 'clsx';
import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

const exampleBefore = `query = """
select user_id, updated_at
from users
qualify row_number() over(partition by user_id order by updated_at desc)=1
"""`;

const exampleAfter = `query = "sql/query.sql"`;

function HomepageHeader() {
  return (
    <header className={styles.hero}>
      <div className="container">
        <div className={styles.heroGrid}>
          <div className={styles.heroCopy}>
            <p className={styles.eyebrow}>Redshift-first Python SQL refactoring</p>
            <Heading as="h1" className={styles.heroTitle}>
              Format and extract Redshift SQL embedded in Python files.
            </Heading>
            <p className={styles.heroSubtitle}>
              pyredsql helps move long triple-quoted SQL strings out of Python code
              and into readable, reviewable SQL files.
            </p>
            <div className={styles.actions}>
              <Link className="button button--primary button--lg" to="/docs/intro">
                Read the docs
              </Link>
              <Link className="button button--secondary button--lg" to="/docs/getting-started/quick-start">
                Quick start
              </Link>
            </div>
          </div>
          <div className={styles.preview} aria-label="pyredsql example">
            <div className={styles.previewHeader}>
              <span>before.py</span>
              <span>pyredsql extract</span>
              <span>after.py</span>
            </div>
            <pre><code>{exampleBefore}</code></pre>
            <div className={styles.arrow}>↓</div>
            <pre><code>{exampleAfter}</code></pre>
          </div>
        </div>
      </div>
    </header>
  );
}

function FeatureCards() {
  const items = [
    {
      title: 'Find embedded SQL',
      body: 'Detect triple-quoted Python strings that look like SQL, including common names such as query, sql, *_query, and *_sql.',
    },
    {
      title: 'Format safely',
      body: 'Use SQLGlot for best-effort Redshift formatting while skipping f-strings and Jinja-like templates by default.',
    },
    {
      title: 'Extract to .sql',
      body: 'Move SQL into external files and replace the Python string with a path reference or Path(...).read_text().',
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <Heading as="h2">Built for practical cleanup work</Heading>
          <p>pyredsql is a refactoring tool, not a database client. It never connects to Redshift or executes SQL.</p>
        </div>
        <div className={styles.cardGrid}>
          {items.map((item) => (
            <article className={styles.card} key={item.title}>
              <Heading as="h3">{item.title}</Heading>
              <p>{item.body}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  return (
    <Layout
      title="pyredsql"
      description="Format and extract Redshift SQL embedded in Python files.">
      <HomepageHeader />
      <FeatureCards />
    </Layout>
  );
}
