# Execução #

## Requisitos ##

- Docker
- Docker Compose

## Instruções ##
1. No arquivo 'docker-compose.yml' adicione seu token de acesso pessoal a API do GitHub na linha 16, substituindo o '???' por ele

2. Na raíz do projeto, onde se encontra o arquivo docker-compose.yml, execute o comando:

```bash
$ docker-compose up
```

## Exportar dados do MongoDB para CSV ##

### Repositórios
```bash
$ mongoexport --host localhost:27017 --authenticationDatabase=admin -u {USER} -p {PASSWORD} --db lab02 --collection github --type=csv --out /csv/repositorios.csv --fields nameWithOwner,url,stargazerCount,createdAt,releases,primaryLanguage,age,processed
```

### Resultados
```bash
$ mongoexport --host localhost:27017 --authenticationDatabase=admin -u {USER} -p {PASSWORD} --db lab02 --collection github --type=csv --out /csv/resultados.csv --fields nameWithOwner,url,stargazerCount,createdAt,releases,primaryLanguage,age,processed,dit,cbo:mean,cbo:median,cbo:std,loc:mean,loc:median,loc:std,lcom*:mean,lcom*:median,lcom*:std --query='{"processed":true}'
```
