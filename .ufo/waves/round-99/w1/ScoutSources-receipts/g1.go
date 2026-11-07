package rules

import (
	"fmt"
	"regexp"
	"strings"
)

// CaseVariant represents the different casing variants for a keyword group.
type CaseVariant string

// KeywordGroupType represents different types of keyword group parsing. This can either be raw or multiple case.
type KeywordGroupType string

const (
	SnakeCase      CaseVariant = "snake_case"
	ConstantCase   CaseVariant = "CONSTANT_CASE"
	KebabCase      CaseVariant = "kebab-case"
	KebabUpperCase CaseVariant = "Kebab-Upper-Case"
	CamelCase      CaseVariant = "camelCase"
	PascalCase     CaseVariant = "PascalCase"
	DotCase        CaseVariant = "dot.case"

	RawKeyword       KeywordGroupType = "raw"
	MultiCaseKeyword KeywordGroupType = "multi_case"

	// assignmentOperand specifies the possible delimiters, used between the LHS and RHS variables in an assignment.
	assignmentOperand = `[="' :>\],\t.()\\?|]{1,10}`
	terminalRegex     = `(?:\\['"rn]|['"\x60; \s]|</|$)`
)

// defaultCaseVariants a list of default case variants to be used when none are specified.
var defaultCaseVariants = []CaseVariant{
	ConstantCase, SnakeCase, CamelCase, KebabCase, DotCase, PascalCase, KebabUpperCase,
}

// kwGroupFormat is the format for `assignmentContext.keywordGroup`
var kwGroupFormat = regexp.MustCompile(`^[a-zA-Z0-9]+(?:\|[a-zA-Z0-9]+)*\|?(?:,[a-zA-Z0-9]+(?:\|[a-zA-Z0-9]+)*\|?)*$`)

type AssignmentRegexOpts struct {
	KeywordGroups    []string
	KeywordGroupType KeywordGroupType
	CaseVariants     []CaseVariant
}

type AssignmentContext struct {
	KeywordGroup     string           `toml:"keywordGroup"`
	KeywordGroups    []string         `toml:"keywordGroups"`
	KeywordGroupType KeywordGroupType `toml:"keywordGroupType"`
	CaseVariants     []CaseVariant    `toml:"caseVariants"`
}

func (a *AssignmentContext) AllKeywordGroups() []string {
	if a.KeywordGroup == "" {
		return a.KeywordGroups
	}
	if len(a.KeywordGroups) == 0 {
		return []string{a.KeywordGroup}
	}
	// Combine both, with KeywordGroup taking precedence for backward compatibility
	result := make([]string, len(a.KeywordGroups)+1)
	copy(result, a.KeywordGroups)
	result[len(a.KeywordGroups)] = a.KeywordGroup
	return result
}

type AssignmentRegexGenResult struct {
	Pattern  string
	Keywords []string
}

type AssignmentRegexGen struct {
	KeywordGroups    []string
	KeywordGroupType KeywordGroupType
	CaseVariants     []CaseVariant
}

func NewAssignmentRegexGen(ctx *AssignmentContext) *AssignmentRegexGen {
	return &AssignmentRegexGen{
		KeywordGroups:    ctx.AllKeywordGroups(),
		KeywordGroupType: ctx.KeywordGroupType,
		CaseVariants:     ctx.CaseVariants,
	}
}

func (a *AssignmentRegexGen) Generate(vendorPattern string) (*AssignmentRegexGenResult, error) {
	if strings.TrimSpace(vendorPattern) == "" {
		return nil, fmt.Errorf("empty vendor pattern passed")
	}

	lhs, keywords, e := a.generateLHSWithKeywords()
	if e != nil {
		return nil, e
	}

	re, err := regexp.Compile(vendorPattern)
	if err != nil {
		return nil, fmt.Errorf("incompatible vendor regex pattern (%q) - %w", vendorPattern, err)
	}

	// remove word boundary since we are adding explicit terminal regex
	vendorPattern = strings.ReplaceAll(vendorPattern, `\b`, "")

	// check if no capture group for vendor pattern then add one surrounding it
	if re.NumSubexp() == 0 {
		vendorPattern = fmt.Sprintf("(%s)", vendorPattern) // wrap within capture group
	}

	return &AssignmentRegexGenResult{
		Pattern:  lhs + assignmentOperand + vendorPattern + terminalRegex,
		Keywords: keywords,
	}, nil
}

func (a *AssignmentRegexGen) validateOrDefault() error {
	if len(a.KeywordGroups) == 0 {
		return fmt.Errorf("empty keyword group")
	}

	if a.KeywordGroupType == "" {
		a.KeywordGroupType = MultiCaseKeyword
	}

	switch a.KeywordGroupType {
	case MultiCaseKeyword:
		for _, kwg := range a.KeywordGroups {
			if !kwGroupFormat.MatchString(kwg) {
				return fmt.Errorf("invalid keyword group format: %s", kwg)
			}
		}
		if len(a.CaseVariants) == 0 {
			a.CaseVariants = defaultCaseVariants
		}
	case RawKeyword:
		if len(a.KeywordGroups) > 1 {
			return fmt.Errorf("only one keyword group is allowed for raw keyword type")
		}
		if len(a.CaseVariants) > 0 {
			return fmt.Errorf("raw keyword group type and case variants are mutually exclusive")
		}
	default:
		return fmt.Errorf("invalid keyword group type: %s", a.KeywordGroupType)
	}

	return nil
}

// generateLHSWithKeywords generates left hand side of the assignment expression along with keywords
func (a *AssignmentRegexGen) generateLHSWithKeywords() (string, []string, error) {
	if e := a.validateOrDefault(); e != nil {
		return "", nil, e
	}

	if a.KeywordGroupType == RawKeyword {
		return a.KeywordGroups[0], nil, nil // no keywords generated for raw type regex keyword group type
	}

	var varNames []string
	for _, kws := range a.KeywordGroups {
		combinations, e := parseKwGroup(kws)
		if e != nil {
			return "", nil, e
		}

		for _, kws := range combinations {
			for _, variant := range a.CaseVariants {
				varNames = append(varNames, genVarName(kws, variant))
			}
		}
	}

	uniqRegexVarNames := unique(varNames, regexp.QuoteMeta)
	lhs := fmt.Sprintf("(?:%s)", strings.Join(uniqRegexVarNames, "|"))
	keywords := unique(varNames, strings.ToLower)

	return lhs, keywords, nil
}

// generates variable name for the ordered combination of keywords based on the given case variant
func genVarName(keywords []string, variant CaseVariant) string {
	switch variant {
	case SnakeCase:
		return toSnakeCase(keywords)
	case CamelCase:
		return toCamelCase(keywords)
	case PascalCase:
		return toPascalCase(keywords)
	case ConstantCase:
		return toConstantCase(keywords)
	case KebabCase:
		return toKebabCase(keywords)
	case DotCase:
		return toDotCase(keywords)
	case KebabUpperCase:
		return toKebabUpperCase(keywords)
	default:
		return ""
	}
}

// parses a keyword group string and returns a list of keyword combinations.
func parseKwGroup(keywordGroup string) ([][]string, error) {
	keywordGroup = strings.TrimSpace(keywordGroup)

	if keywordGroup == "" {
		return nil, fmt.Errorf("empty keywordGroup")
	}

	prevs := [][]string{nil}

	for _, part := range strings.Split(keywordGroup, ",") {
		alts := strings.Split(part, "|")

		hasEmpty := false
		var nexts [][]string
		for _, alt := range alts {
			alt = strings.TrimSpace(alt)

			if alt == "" {
				hasEmpty = true
				continue
			}

			for _, prev := range prevs {
				nexts = append(nexts, append(prev, alt))
			}
		}

		if hasEmpty {
			prevs = append(prevs, nexts...)
		} else {
			prevs = nexts
		}
	}

	result := prevs
	if len(result) > 0 && result[0] == nil {
		result = result[1:]
	}

	if len(result) == 0 {
		return nil, fmt.Errorf("keywordGroup is empty after parse")
	}

	return result, nil
}

func toCamelCase(kw []string) string {
	var sb strings.Builder
	for i, w := range kw {
		if i == 0 {
			sb.WriteString(toggleFirstCharCase(w, true /*toLower*/))
		} else {
			sb.WriteString(toggleFirstCharCase(w, false /*toLower*/))
		}
	}
	return sb.String()
}

func toPascalCase(kw []string) string {
	return formatCase(kw, rune(0), func(s string) string {
		return toggleFirstCharCase(s, false /*toLower*/)
	})
}

func toSnakeCase(kw []string) string {
	return formatCase(kw, '_', strings.ToLower)
}

func toConstantCase(kw []string) string {
	return formatCase(kw, '_', strings.ToUpper)
}

func toKebabCase(kw []string) string {
	return formatCase(kw, '-', strings.ToLower)
}

func toKebabUpperCase(kw []string) string {
	return formatCase(kw, '-', func(s string) string { return toggleFirstCharCase(s, false /*toLower*/) })
}

func toDotCase(kw []string) string {
	return formatCase(kw, '.', strings.ToLower)
}

func formatCase(kw []string, separator rune, modifier func(s string) string) string {
	var sb strings.Builder
	for i, w := range kw {
		sb.WriteString(modifier(w))
		if separator != 0 && i < len(kw)-1 {
			sb.WriteRune(separator)
		}
	}
	return sb.String()
}

func toggleFirstCharCase(s string, toLower bool) string {
	if len(s) == 0 {
		return s
	}
	val := []byte(s)
	b := val[0]
	if toLower {
		if b >= 'A' && b <= 'Z' { // lower case the first letter
			val[0] = b + 32
		}
	} else {
		if b >= 'a' && b <= 'z' { // capitalize the first letter
			val[0] = b - 32
		}
	}
	return string(val)
}

// takes values and returns slice of unique elements. It optinally accepts a transformation
// function that is run on the element before applying uniqueness logic to it.
func unique(values []string, transformFunc func(s string) string) []string {
	seen := make(map[string]struct{})
	var names []string
	for _, v := range values {
		if transformFunc != nil {
			v = transformFunc(v)
		}
		if v == "" {
			continue
		}
		if _, exists := seen[v]; !exists {
			seen[v] = struct{}{}
			names = append(names, v)
		}
	}
	return names
}

// SetAssignmentCtxFields sets generated assignment regex to `regex` property of each rule
// and also sets combination of variable names to `keywords` property of each rule
func SetAssignmentCtxFields(rules []*Rule) error {
	for i := range rules {
		if e := setAssignmentCtxFields(rules[i]); e != nil {
			return e
		}
	}
	return nil
}

// setAssignmentCtxFields generates assignment regex and sets it to the `regex` property of the given
// rule and also sets combination of variable names to `keywords` property.
func setAssignmentCtxFields(rule *Rule) error {
	if rule.AssignmentCtx == nil {
		return nil
	}
	regexGen := NewAssignmentRegexGen(rule.AssignmentCtx)
	res, e := regexGen.Generate(rule.Regex)
	if e != nil {
		return fmt.Errorf("assignment regex gen failed for rule(%s): %w", rule.ID, e)
	}
	rule.Regex = res.Pattern
	rule.Keywords = unique(append(rule.Keywords, res.Keywords...), strings.ToLower) // append to user-defined keywords (if any) and ensure uniqueness while merging both set of keywods
	return nil
}
