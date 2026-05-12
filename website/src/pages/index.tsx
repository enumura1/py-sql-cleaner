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
            <div className={styles.previewTitle}>
              <span className={styles.previewKicker}>Example workflow</span>
              <strong>Extract embedded SQL from Python</strong>
            </div>
            <div className={styles.previewStep}>
              <span>Before: SQL lives inside Python</span>
              <pre><code>{exampleBefore}</code></pre>
            </div>
            <div className={styles.previewStep}>
              <span>Run</span>
              <pre><code>pyredsql extract jobs/load_users.py --out-dir sql</code></pre>
            </div>
            <div className={styles.previewStep}>
              <span>After: Python points to the SQL file</span>
              <pre><code>{exampleAfter}</code></pre>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

function FeatureList() {
  const items = [
    {
      step: '01',
      title: 'Find embedded SQL',
      body: 'Scan Python files for triple-quoted strings that look like SQL. pyredsql combines SQL-like keywords with common variable names such as query, sql, *_query, and *_sql.',
      command: 'pyredsql list jobs/load_users.py',
    },
    {
      step: '02',
      title: 'Format safely',
      body: 'Format Redshift SQL through SQLGlot while keeping runtime-sensitive strings untouched. f-strings and Jinja-like templates are detected, reported, and skipped by default.',
      command: 'pyredsql format jobs/load_users.py --dry-run',
    },
    {
      step: '03',
      title: 'Extract to .sql',
      body: 'Move large embedded queries into external .sql files. The Python side can be replaced with a path string, or with Path(...).read_text() when that fits your project.',
      command: 'pyredsql extract jobs/load_users.py --out-dir sql',
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <Heading as="h2">Built for practical cleanup work</Heading>
          <p>pyredsql is a refactoring tool, not a database client. It never connects to Redshift or executes SQL.</p>
        </div>
        <div className={styles.featureList}>
          {items.map((item) => (
            <article className={styles.featureItem} key={item.title}>
              <div className={styles.stepBadge}>{item.step}</div>
              <div className={styles.featureBody}>
                <Heading as="h3">{item.title}</Heading>
                <p>{item.body}</p>
              </div>
              <pre className={styles.command}><code>{item.command}</code></pre>
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
      <FeatureList />
    </Layout>
  );
}
