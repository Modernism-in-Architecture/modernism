#!/bin/sh

function check_url() {
    url=$1
    echo "TEST ${url}"
    time curl -so --silent -w "http code: %{http_code}" --location ${url} --header "Authorization: Token ${MIA_API_TOKEN}"
    echo
}

if [[ ! ${MIA_API_TOKEN+x} ]]; then
    echo "MIA_API_TOKEN not set in environment"
    exit 1
fi

check_url "https://modernism-in-architecture.org/api/v1/buildings"
check_url "https://modernism-in-architecture.org/api/v1/buildings/828"

check_url "https://modernism-in-architecture.org/api/v1/architects"
check_url "https://modernism-in-architecture.org/api/v1/architects/867"
