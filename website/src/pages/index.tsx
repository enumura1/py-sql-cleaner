import Link from '@docusaurus/Link';
import Heading from '@theme/Heading';
import Layout from '@theme/Layout';
import type {JSX, ReactNode} from 'react';
import styles from './index.module.css';

type CodeLanguage = 'python' | 'sql';

const heroBefore = `query = """
select user_id, sum(amount)
from analytics.orders
where status='paid'
"""`;

const heroPythonAfter = `query = "sql/paid_users.sql"`;

const heroSqlAfter = `SELECT
  user_id,
  SUM(amount)
FROM analytics.orders
WHERE status = 'paid'
GROUP BY user_id`;

const sqlKeywords = new Set([
  'AND',
  'AS',
  'BY',
  'COUNT',
  'CURRENT_DATE',
  'DATEADD',
  'DAY',
  'DESC',
  'FROM',
  'GROUP',
  'HAVING',
  'JOIN',
  'LIMIT',
  'ON',
  'ORDER',
  'OVER',
  'PARTITION',
  'QUALIFY',
  'ROW_NUMBER',
  'SELECT',
  'SUM',
  'WHERE',
]);

function tokenize(
  line: string,
  pattern: RegExp,
  getClassName: (token: string) => string | undefined,
) {
  const pieces: ReactNode[] = [];
  let lastIndex = 0;

  line.replace(pattern, (token, ...args) => {
    const offset = args[args.length - 2] as number;

    if (offset > lastIndex) {
      pieces.push(line.slice(lastIndex, offset));
    }

    const className = getClassName(token);
    pieces.push(
      className ? (
        <span className={className} key={`${offset}-${token}`}>
          {token}
        </span>
      ) : (
        token
      ),
    );
    lastIndex = offset + token.length;
    return token;
  });

  if (lastIndex < line.length) {
    pieces.push(line.slice(lastIndex));
  }

  return pieces;
}

function highlightSqlLine(line: string) {
  return tokenize(
    line,
    /--.*$|'[^']*'|\b[A-Z_]+\b|\b[a-z_]+\b|\b\d+\b/g,
    (token) => {
      if (token.startsWith('--')) return styles.codeComment;
      if (token.startsWith("'")) return styles.codeString;
      if (/^\d+$/.test(token)) return styles.codeNumber;
      if (sqlKeywords.has(token.toUpperCase())) return styles.codeKeyword;
      return undefined;
    },
  );
}

function highlightPythonLine(line: string, inSqlString: boolean) {
  if (inSqlString) {
    return highlightSqlLine(line);
  }

  return tokenize(
    line,
    /#.*$|"""|"[^"]*"|'[^']*'|\b(users_query|sessions_query|query)\b|[=()]/g,
    (token) => {
      if (token.startsWith('#')) return styles.codeComment;
      if (token === '"""' || token.startsWith('"') || token.startsWith("'")) {
        return styles.codeString;
      }
      if (['query', 'users_query', 'sessions_query'].includes(token)) {
        return styles.codeVariable;
      }
      if (/^[=()]$/.test(token)) return styles.codeOperator;
      return undefined;
    },
  );
}

function PromptLine({children, className}: {children: ReactNode; className?: string}) {
  return (
    <div className={`${styles.promptLine} ${className ?? ''}`}>
      <span aria-hidden="true">$</span>
      <code>{children}</code>
    </div>
  );
}

function SyntaxBlock({
  language,
  children,
}: {
  language: CodeLanguage;
  children: string;
}) {
  let inSqlString = false;
  const lines = children.split('\n');

  return (
    <div className={styles.syntaxBlock}>
      <pre>
        <code>
          {lines.map((line, index) => {
            const delimiterLine = language === 'python' && line.includes('"""');
            const shouldHighlightAsSql = language === 'sql' || (inSqlString && !delimiterLine);
            const renderedLine =
              language === 'sql'
                ? highlightSqlLine(line)
                : highlightPythonLine(line, shouldHighlightAsSql);

            if (delimiterLine) {
              inSqlString = !inSqlString;
            }

            return (
              <span className={styles.codeLine} key={`${index}-${line}`}>
                {renderedLine}
                {index < lines.length - 1 ? '\n' : null}
              </span>
            );
          })}
        </code>
      </pre>
    </div>
  );
}

function FileTypeIcon({kind}: {kind: 'python' | 'sql' | 'terminal'}) {
  return (
    <span className={`${styles.fileTypeIcon} ${styles[`fileTypeIcon_${kind}`]}`} aria-hidden="true">
      {kind === 'python' ? 'py' : kind === 'sql' ? 'sql' : '$'}
    </span>
  );
}

function WorkflowConnector() {
  return <div className={styles.workflowConnector} aria-hidden="true" />;
}

function HomepageHeader() {
  return (
    <header className={styles.hero}>
      <div className="container">
        <div className={styles.heroGrid}>
          <div className={styles.heroCopy}>
            <p className={styles.eyebrow}>Python embedded SQL cleanup</p>
            <Heading as="h1" className={styles.heroTitle}>
              py-sql-cleaner
            </Heading>
            <p className={styles.heroSubtitle}>
              Clean up Python files that hide SQL in triple-quoted strings. Scan
              them, format safe queries, or extract long queries into reviewable
              SQL files.
            </p>
            <div className={styles.actions}>
              <Link className="button button--primary button--lg" to="/docs/intro">
                Read the docs
              </Link>
              <Link
                className="button button--secondary button--lg"
                to="/docs/getting-started/quick-start">
                Quick start
              </Link>
            </div>
          </div>
          <div className={styles.preview} aria-label="py-sql-cleaner extraction workflow">
            <div className={styles.workflowTrack}>
              <div className={styles.workflowNode}>
                <div className={styles.workflowNodeHeader}>
                  <FileTypeIcon kind="python" />
                  <div>
                    <span>Step 1 &middot; Before</span>
                    <strong>jobs/load_paid_users.py</strong>
                  </div>
                </div>
                <SyntaxBlock language="python">{heroBefore}</SyntaxBlock>
              </div>
              <WorkflowConnector />
              <div className={`${styles.workflowNode} ${styles.workflowRunNode}`}>
                <div className={styles.workflowNodeHeader}>
                  <FileTypeIcon kind="terminal" />
                  <div>
                    <span>Step 2 &middot; Run</span>
                    <strong>extract command</strong>
                  </div>
                </div>
                <div className={styles.runTerminal}>
                  <div className={styles.runTerminalChrome} aria-hidden="true">
                    <span />
                    <span />
                    <span />
                    <span className={styles.runTerminalTitle}>terminal</span>
                  </div>
                  <PromptLine className={styles.heroPrompt}>
                    py-sql-cleaner extract jobs/load_paid_users.py --out-dir sql
                  </PromptLine>
                </div>
              </div>
              <WorkflowConnector />
              <div className={styles.workflowNode}>
                <div className={styles.workflowNodeHeader}>
                  <FileTypeIcon kind="sql" />
                  <div>
                    <span>Step 3 &middot; After</span>
                    <strong>Python reference + new SQL file</strong>
                  </div>
                </div>
                <div className={styles.heroAfterGrid}>
                  <div className={styles.heroAfterPane}>
                    <div className={styles.heroAfterPaneLabel}>
                      <FileTypeIcon kind="python" />
                      <code>jobs/load_paid_users.py</code>
                    </div>
                    <SyntaxBlock language="python">{heroPythonAfter}</SyntaxBlock>
                  </div>
                  <div className={styles.heroAfterPane}>
                    <div className={styles.heroAfterPaneLabel}>
                      <FileTypeIcon kind="sql" />
                      <code>sql/paid_users.sql</code>
                    </div>
                    <SyntaxBlock language="sql">{heroSqlAfter}</SyntaxBlock>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}

const listRows = [
  {file: 'jobs/load_users.py:14', name: 'users_query', lines: '18 lines', status: 'safe'},
  {file: 'jobs/load_users.py:42', name: 'events_sql', lines: '24 lines', status: 'safe'},
  {file: 'jobs/sessions.py:11', name: 'sessions_query', lines: '31 lines', status: 'skip', reason: 'f-string'},
  {file: 'jobs/orders.py:67', name: 'orders_sql', lines: '12 lines', status: 'safe'},
  {file: 'jobs/cohorts.py:29', name: 'cohort_query', lines: '44 lines', status: 'skip', reason: 'jinja'},
];

const findExample = `# jobs/load_users.py
users_query = """
select user_id, email from analytics.users
"""

# jobs/sessions.py
sessions_query = f"""
select * from sessions where ds = '{run_date}'
"""`;

const formatBefore = `query = """
select u.user_id,u.email,count(o.order_id) as paid_orders,
sum(o.amount) as revenue
from analytics.users u join analytics.orders o on o.user_id=u.user_id
where o.status='paid' and o.created_at>=dateadd(day,-30,current_date)
group by u.user_id,u.email
having sum(o.amount)>100
order by revenue desc limit 50
"""`;

const formatAfter = `query = """
SELECT
  u.user_id,
  u.email,
  COUNT(o.order_id) AS paid_orders,
  SUM(o.amount) AS revenue
FROM analytics.users AS u
JOIN analytics.orders AS o
  ON o.user_id = u.user_id
WHERE
  o.status = 'paid'
  AND o.created_at >= DATEADD(DAY, -30, CURRENT_DATE)
GROUP BY
  u.user_id,
  u.email
HAVING SUM(o.amount) > 100
ORDER BY revenue DESC
LIMIT 50
"""`;

const extractBefore = `# jobs/load_users.py
query = """
  select user_id, updated_at
  from analytics.users
  qualify row_number() over(
    partition by user_id
    order by updated_at desc
  ) = 1
"""`;

const extractPythonAfter = `# jobs/load_users.py
query = "sql/load_users.sql"`;

const extractSqlAfter = `-- sql/load_users.sql
SELECT
  user_id,
  updated_at
FROM analytics.users
QUALIFY ROW_NUMBER() OVER (
  PARTITION BY user_id
  ORDER BY updated_at DESC
) = 1`;

const findDetails = [
  {
    title: 'Maps the cleanup surface',
    body: 'Shows file, variable name, line count, and whether the block is safe to rewrite.',
  },
  {
    title: 'Separates safe from risky',
    body: 'Plain strings are marked safe. f-strings and Jinja-like templates are visible but skipped.',
  },
  {
    title: 'Read-only by design',
    body: 'The list command changes nothing, so you can inspect a project before choosing a cleanup command.',
  },
];

const formatDetails = [
  {
    title: 'Keeps the query in place',
    body: 'Only the SQL body changes. The Python variable and surrounding code stay where they are.',
  },
  {
    title: 'Preview before writing',
    body: 'Dry-run shows the diff. Check mode makes the same rule usable in CI.',
  },
  {
    title: 'Protects dynamic SQL',
    body: 'Runtime-sensitive strings are skipped by default instead of being reformatted blindly.',
  },
];

const extractDetails = [
  {
    title: 'Shrinks the Python file',
    body: 'The long string becomes a path reference, so the job code is easier to scan.',
  },
  {
    title: 'Creates a real SQL artifact',
    body: 'The query gets its own SQL file, with cleaner diffs and normal editor support.',
  },
  {
    title: 'Formats while extracting',
    body: 'Safe blocks are formatted as they move. Unsafe blocks remain visible but untouched.',
  },
];

const introPoints = [
  {
    label: 'It does not execute SQL',
    text: 'The tool only reads and rewrites files. There is no database connection, credential handling, or query execution path.',
  },
  {
    label: 'It starts with inventory',
    text: 'List shows which embedded queries exist and which ones are safe before any rewrite command runs.',
  },
  {
    label: 'It keeps risky templates visible',
    text: 'f-strings and Jinja-like SQL are reported as skipped so cleanup work does not hide runtime behavior.',
  },
];

function TerminalListPreview() {
  return (
    <div className={styles.terminalPreview}>
      <PromptLine>py-sql-cleaner list jobs/</PromptLine>
      <div className={styles.resultTable} role="table" aria-label="py-sql-cleaner list output">
        {listRows.map((row) => (
          <div className={styles.resultRow} role="row" key={`${row.file}-${row.name}`}>
            <code className={styles.resultFile}>{row.file}</code>
            <code className={styles.resultName}>{row.name}</code>
            <span className={styles.resultLines}>{row.lines}</span>
            <span className={row.status === 'safe' ? styles.safePill : styles.skipPill}>
              {row.status}
              {row.reason ? <span> · {row.reason}</span> : null}
            </span>
          </div>
        ))}
      </div>
      <div className={styles.resultSummary}>
        <strong>Found 5 blocks</strong>
        <span>3 safe</span>
        <span>2 skipped</span>
      </div>
    </div>
  );
}

function DetailList({
  items,
}: {
  items: {
    title: string;
    body: string;
  }[];
}) {
  return (
    <div className={styles.detailList}>
      {items.map((item) => (
        <div className={styles.detailItem} key={item.title}>
          <strong>{item.title}</strong>
          <p>{item.body}</p>
        </div>
      ))}
    </div>
  );
}

function CodePane({
  label,
  filename,
  language,
  children,
}: {
  label: string;
  filename: string;
  language: CodeLanguage;
  children: string;
}) {
  return (
    <div className={styles.codePane}>
      <div className={styles.codePaneHeader}>
        <span className={styles.codePaneLabel}>
          <FileTypeIcon kind={language} />
          {label}
        </span>
        <code>{filename}</code>
      </div>
      <SyntaxBlock language={language}>{children}</SyntaxBlock>
    </div>
  );
}

type CodePaneData = {
  label: string;
  filename: string;
  language: CodeLanguage;
  code: string;
};

function BeforeAfterPreview({
  beforeBlock,
  afterBlocks,
  commandLabel,
}: {
  beforeBlock: CodePaneData;
  afterBlocks: CodePaneData[];
  commandLabel?: string;
}) {
  return (
    <div className={styles.beforeAfterPreview}>
      <div className={styles.previewSplit}>
        <CodePane
          label={beforeBlock.label}
          filename={beforeBlock.filename}
          language={beforeBlock.language}>
          {beforeBlock.code}
        </CodePane>
        <div className={styles.previewBridge}>
          {commandLabel ? (
            <span className={styles.previewBridgeLabel}>
              <span className={styles.previewBridgePrompt} aria-hidden="true">$</span>
              {commandLabel}
            </span>
          ) : null}
          <div className={styles.previewArrow} aria-hidden="true">→</div>
        </div>
        <div className={styles.afterStack}>
          {afterBlocks.map((block) => (
            <CodePane
              key={`${block.filename}-${block.label}`}
              label={block.label}
              filename={block.filename}
              language={block.language}>
              {block.code}
            </CodePane>
          ))}
        </div>
      </div>
    </div>
  );
}

function FeatureList() {
  const items = [
    {
      step: '01',
      title: 'Find embedded SQL',
      summary: 'First, get a read-only inventory of SQL hidden in Python files.',
      body: 'Find triple-quoted strings that look like SQL, then separate safe blocks from dynamic templates before cleanup begins.',
      command: 'py-sql-cleaner list jobs/',
      previewLabel: 'Input Python and scan result',
      details: findDetails,
      preview: (
        <div className={styles.findPreview}>
          <CodePane label="Example input" filename="jobs/*.py" language="python">
            {findExample}
          </CodePane>
          <TerminalListPreview />
        </div>
      ),
    },
    {
      step: '02',
      title: 'Format SQL inside Python',
      summary: 'Clean up embedded SQL without moving it out of the Python file.',
      body: 'Rewrite only the SQL text inside a Python string. Use it when the query should stay embedded but still needs readable formatting.',
      command: 'py-sql-cleaner format jobs/load_paid_users.py --dry-run',
      previewLabel: 'Before and after',
      details: formatDetails,
      preview: (
        <BeforeAfterPreview
          commandLabel="format"
          beforeBlock={{
            label: 'Before',
            filename: 'jobs/load_paid_users.py',
            language: 'python',
            code: formatBefore,
          }}
          afterBlocks={[
            {
              label: 'After',
              filename: 'jobs/load_paid_users.py',
              language: 'python',
              code: formatAfter,
            },
          ]}
        />
      ),
    },
    {
      step: '03',
      title: 'Extract to .sql',
      summary: 'Move large queries from Python into real SQL files.',
      body: 'Use extraction when a query should be reviewed as SQL, not as a giant Python string. Python keeps a small reference; SQL gets its own file.',
      command: 'py-sql-cleaner extract jobs/load_users.py --out-dir sql',
      previewLabel: 'Python file becomes Python + SQL file',
      details: extractDetails,
      preview: (
        <BeforeAfterPreview
          commandLabel="extract"
          beforeBlock={{
            label: 'Before',
            filename: 'jobs/load_users.py',
            language: 'python',
            code: extractBefore,
          }}
          afterBlocks={[
            {
              label: 'After',
              filename: 'jobs/load_users.py',
              language: 'python',
              code: extractPythonAfter,
            },
            {
              label: 'New SQL file',
              filename: 'sql/load_users.sql',
              language: 'sql',
              code: extractSqlAfter,
            },
          ]}
        />
      ),
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className={styles.sectionHeader}>
          <span className={styles.sectionEyebrow}>How it works</span>
          <Heading as="h2">Three cleanup jobs, one workflow</Heading>
          <p>
            py-sql-cleaner targets the cleanup work that piles up after a Python
            job has accumulated large embedded queries. Find the strings, format
            the safe ones in place, and move review-worthy queries into real SQL
            files.
          </p>
          <div className={styles.introGrid}>
            {introPoints.map((point) => (
              <div className={styles.introPoint} key={point.label}>
                <strong>{point.label}</strong>
                <span>{point.text}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className={styles.featureList}>
        {items.map((item) => (
          <article className={styles.featureItem} key={item.title}>
            <div className="container">
              <div className={styles.featureGrid}>
                <div className={styles.featureText}>
                  <div className={styles.featureHeader}>
                    <div className={styles.stepBadge}>{item.step}</div>
                    <div className={styles.featureBody}>
                      <p className={styles.featureSummary}>{item.summary}</p>
                      <Heading as="h3">{item.title}</Heading>
                      <p>{item.body}</p>
                    </div>
                  </div>
                  <div className={styles.command}>
                    <span>Run</span>
                    <PromptLine>{item.command}</PromptLine>
                  </div>
                  <DetailList items={item.details} />
                </div>
                <div className={styles.featurePreview} aria-label={`${item.title} example`}>
                  <div className={styles.featurePreviewHeader}>{item.previewLabel}</div>
                  <div className={styles.featurePreviewBody}>{item.preview}</div>
                </div>
              </div>
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  return (
    <Layout
      title="py-sql-cleaner"
      description="Find, format, and extract SQL embedded in Python files.">
      <HomepageHeader />
      <FeatureList />
    </Layout>
  );
}
