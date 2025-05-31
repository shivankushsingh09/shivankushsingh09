import os
import base64
import requests
from github import Github
from collections import defaultdict

# Get GitHub token
token = os.getenv('GITHUB_TOKEN')
g = Github(token)

# Get authenticated user
user = g.get_user()

# Get all repositories
repos = user.get_repos()

# Dictionary to store language bytes
language_bytes = defaultdict(int)

total_bytes = 0

# Calculate language usage across all repositories
for repo in repos:
    if not repo.fork:  # Only count non-forked repositories
        try:
            langs = repo.get_languages()
            for lang, bytes_count in langs.items():
                language_bytes[lang] += bytes_count
                total_bytes += bytes_count
        except Exception as e:
            print(f"Error processing {repo.name}: {str(e)}")

# Calculate percentages
language_percentages = {}
for lang, bytes_count in language_bytes.items():
    percentage = (bytes_count / total_bytes) * 100
    language_percentages[lang] = round(percentage, 1)

# Sort languages by percentage (descending)
sorted_languages = sorted(
    language_percentages.items(), 
    key=lambda x: x[1], 
    reverse=True
)

# Generate markdown content
markdown = "## 🛠️ Technology Usage\n\n"
markdown += "Here's a breakdown of the programming languages and technologies I use across my repositories:\n\n"
markdown += "<div align=\"center\">\n"
markdown += "<table>\n"
markdown += "  <tr>\n    <th>Language</th>\n    <th>Usage</th>\n    <th>Progress</th>\n  </tr>\n"

# GitHub language colors (you can add more as needed)
language_colors = {
    'Python': '#3572A5',
    'JavaScript': '#f1e05a',
    'TypeScript': '#2b7489',
    'HTML': '#e34c26',
    'CSS': '#563d7c',
    'Java': '#b07219',
    'C++': '#f34b7d',
    'C': '#555555',
    'C#': '#178600',
    'PHP': '#4F5D95',
    'Go': '#00ADD8',
    'Rust': '#dea584',
    'Ruby': '#701516',
    'Swift': '#ffac45',
    'Kotlin': '#A97BFF',
    'Dart': '#00B4AB',
    'Scala': '#c22d40',
    'Shell': '#89e051',
    'PowerShell': '#012456',
    'Objective-C': '#438eff',
    'R': '#198CE7',
    'Vue': '#41b883',
    'Dockerfile': '#384d54',
    'Makefile': '#427819',
    'TeX': '#3D6117',
    'Vim script': '#199f4b',
    'Lua': '#000080',
    'Perl': '#0298c3',
    'Haskell': '#5e5086',
    'OCaml': '#3be133',
    'Clojure': '#db5855',
    'Elixir': '#6e4a7e',
    'Elm': '#60B5CC',
    'Erlang': '#B83998',
    'F#': '#b845fc',
    'Groovy': '#e69f56',
    'Julia': '#a270ba',
    'Nim': '#ffc200',
    'Perl 6': '#0000fb',
    'Roff': '#ecdebe',
    'Zig': '#ec915c'
}

for lang, percentage in sorted_languages:
    if percentage < 0.1:  # Skip languages with less than 0.1%
        continue
        
    color = language_colors.get(lang, '#cccccc')
    progress_width = int(percentage * 2)  # Scale for better visibility
    
    markdown += f"""  <tr>
    <td><span style="font-weight:bold;">{lang}</span></td>
    <td>{percentage}%</td>
    <td>
      <div style="width: 300px; background-color: #e0e0e0; border-radius: 5px;">
        <div style="width: {progress_width}%; background-color: {color}; height: 10px; border-radius: 5px;"></div>
      </div>
    </td>
  </tr>
"""

markdown += """</table>
</div>

*Updated automatically using [GitHub Actions](.github/workflows/update-languages.yml)*
"""

# Update README.md
with open('README.md', 'r', encoding='utf-8') as file:
    content = file.read()

# Find the Technology Usage section or add it at the end
if '## 🛠️ Technology Usage' in content:
    # Replace existing section
    start = content.find('## 🛠️ Technology Usage')
    next_heading = content.find('## ', start + 1)
    if next_heading == -1:
        content = content[:start] + markdown
    else:
        content = content[:start] + markdown + content[next_heading:]
else:
    # Add new section before the first heading
    first_heading = content.find('## ')
    if first_heading != -1:
        content = content[:first_heading] + markdown + '\n\n' + content[first_heading:]
    else:
        content += '\n\n' + markdown

# Write the updated content back to README.md
with open('README.md', 'w', encoding='utf-8') as file:
    file.write(content)

print("Successfully updated README.md with language statistics!")
