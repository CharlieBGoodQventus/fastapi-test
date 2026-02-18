{{/*
Expand the name of the chart.
*/}}
{{- define "fast-api-test.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "fast-api-test.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "fast-api-test.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "fast-api-test.labels" -}}
helm.sh/chart: {{ include "fast-api-test.chart" . }}
{{ include "fast-api-test.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "fast-api-test.selectorLabels" -}}
app.kubernetes.io/name: {{ include "fast-api-test.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "fast-api-test.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "fast-api-test.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Extract directory path from a file path
*/}}
{{- define "fast-api-test.dir" -}}
{{- $path := . }}
{{- if hasSuffix "/" $path }}
{{- trimSuffix "/" $path }}
{{- else }}
{{- regexReplaceAll "/[^/]+$" $path "" }}
{{- end }}
{{- end }}

{{/*
Create the name of the certificate to use
*/}}
{{- define "fast-api-test.certificateName" -}}
{{- printf "%s-tls" (include "fast-api-test.fullname" .) }}
{{- end }}

{{/*
Create the name of the ssm secrets to use
*/}}
{{- define "fast-api-test.ssmSecretsName" -}}
{{- printf "%s-ssm" (include "fast-api-test.fullname" .) }}
{{- end }}

{{/*
Create the name of the secrets manager secrets to use
*/}}
{{- define "fast-api-test.smSecretsName" -}}
{{- printf "%s-sm" (include "fast-api-test.fullname" .) }}
{{- end }}
