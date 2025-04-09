\ProvidesClass{cvtemplate}[2025/04/04 v1.0 Custom CV Class]

% Base class and font size
\LoadClass[10pt]{article}

% Layout packages
\usepackage[parfill]{parskip} % No indentation at the start of paragraphs
\usepackage{array}            % Bold tabular columns
\usepackage{ifthen}           % Logic control for conditionals

% No page numbering
\pagestyle{empty}

% ======================
% Personal Header Setup
% ======================

\def \setname#1{\def\cv@name{#1}}
\def \cv@name {}
\def \sep {$\diamond$}

% Initialize optional contact lines
\let \lineone \relax
\let \linetwo \relax
\let \linethree \relax

% Command to assign contact details, supports 1 to 3 lines
\def \contactinfo #1{
  \@ifundefined{linetwo}{
    \def \linetwo {#1}
  }{
  \@ifundefined{linethree}{
    \def \linethree {#1}
  }{
    \def \lineone {#1}
  }}
}

% Command to print a single line of contact
\def \showline #1{
  \begingroup
    \def \\ {\sep\ }
    \centerline{#1}
  \endgroup
  \gapafterline
}

% Name display at top
\def \displayname {
  \begingroup
    \hfil{\MakeUppercase{\nameformat\bf \cv@name}}\hfil
    \gapaftername\break
  \endgroup
}

% ======================
% Automatic Header Output
% ======================

\let\original@document=\document
\renewcommand{\document}{
  \original@document
  \displayname
  \@ifundefined{lineone}{}{\showline{\lineone}}
  \@ifundefined{linetwo}{}{\showline{\linetwo}}
  \@ifundefined{linethree}{}{\showline{\linethree}}
}

% ======================
% Section Title Styling
% ======================

\newenvironment{Section}[1]{
  \MakeUppercase{\textbf{#1}}
  \gapbeforeline
  \hrule
  \begin{list}{}{
    \setlength{\leftmargin}{1.5em}
  }
  \item[]
}{
  \end{list}
}

% ======================
% Work Experience Format
% ======================

\newenvironment{Experience}[4]{ % org, date, title, location
  {\textbf{#1}} \hfill {#2}
  \ifthenelse{\equal{#3}{}}{}{
    \\
    \textbf{\emph{#3}} \hfill \textbf{\emph{#4}}
  }\smallskip
  \begin{list}{$\cdot$}{\leftmargin=0.75em}
    \itemsep -0.4em \vspace{-0.75em}
}{
  \end{list}
}

\newenvironment{AdditionalWork}[2]{ % title, date
  {\textbf{\emph{#1}}} \hfill \textbf{#2}
  \smallskip
  \begin{list}{$\cdot$}{\leftmargin=0.75em}
    \itemsep -0.4em \vspace{-0.75em}
}{
  \end{list}
}

% ======================
% Spacing and Font Sizes
% ======================

\def\nameformat{\Large}
\def\gapafterline{\smallskip}
\def\gapbeforeline{\medskip}
\def\gapaftername{\bigskip}
\def\gapaftersection{\medskip}
