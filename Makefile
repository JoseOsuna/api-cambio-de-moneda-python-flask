DCMP = docker-compose
APP = gobanx_api
DCMP_EXEC_APP = ${DCMP} exec ${APP}
DCMP_RUN_APP = ${DCMP} run ${APP}

up:
	${DCMP} up

down:
	${DCMP} down

bash:
	${DCMP_EXEC_APP} bash
