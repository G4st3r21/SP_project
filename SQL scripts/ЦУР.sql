--
--DROP TABLE CYR;
--DROP TABLE TASKS_CYR;
--DROP TABLE INDICATIONS_RF;
--DROP TABLE RESPONSE_OBJ;
--DROP TABLE INDICATIONS_VO;
--DROP TABLE INDICATIONS_RF_VO;
--DROP TABLE GOSPROGRAM_VO
--DROP TABLE TARGET_GOSPROGRAM_VO;
--DROP TABLE GOSPROGRAM_TARGET;
--DROP TABLE INDICATIONS_RF_TARGET;
--

DROP TABLE GOSPROGRAM_TASKS;
DROP TABLE GOSPROGRAM_AND_TASKS;

--
--CREATE TABLE CYR
--  (id INTEGER PRIMARY KEY,
--  title_cyr TEXT NOT NULL);
--
--CREATE TABLE TASKS_CYR
--  (id INTEGER PRIMARY KEY,
--  id_cyr INTEGER REFERENCES CYR(id),
--  task TEXT NOT NULL);
--
--CREATE TABLE INDICATIONS_RF
--  (id INTEGER PRIMARY KEY,
--  id_task INTEGER REFERENCES TASKS(id),
--  ind_title_rf TEXT NOT NULL);
--
--CREATE TABLE RESPONSE_OBJ
--  (id INTEGER PRIMARY KEY,
--  response_obj TEXT NOT NULL);
--
--CREATE TABLE INDICATIONS_VO
--  (id INTEGER PRIMARY KEY,
--  id_response INTEGER REFERENCES RESPONSE_OBJ(id),
--  ind_title_vo TEXT NOT NULL);
--
--CREATE TABLE INDICATIONS_RF_VO
--  (id_ind_rf INTEGER REFERENCES INDICATIONS_RF(id),
--  id_ind_vo INTEGER REFERENCES INDICATIONS_VO(id),
--CONSTRAINT IND_RF_VO_PK
--  PRIMARY KEY (id_ind_rf, id_ind_vo));
--
--CREATE TABLE GOSPROGRAM_VO
--  (id INTEGER PRIMARY KEY,
--  title_prog TEXT NOT NULL,
--  id_response INTEGER REFERENCES RESPONSE_OBJ(id),
--  id_ind_rf INTEGER REFERENCES INDICATIONS_RF(id),
--  id_ind_vo INTEGER REFERENCES INDICATIONS_VO(id),
--  UNIQUE (id_ind_rf, id_ind_vo));
--
--CREATE TABLE TARGET_GOSPROGRAM_VO
--  (id INTEGER PRIMARY KEY,
--  target TEXT NOT NULL);
--
--CREATE TABLE GOSPROGRAM_TARGET
--  (id_prog INTEGER REFERENCES GOSPROGRAM_VO(id),
--  id_target INTEGER REFERENCES TARGET_GOSPROGRAM_VO(id),
--CONSTRAINT GOSPROGRAM_TARGET_PK
--  PRIMARY KEY (id_prog, id_target));
--
--CREATE TABLE INDICATIONS_RF_TARGET
--  (id_ind_rf INTEGER REFERENCES INDICATIONS_RF(id),
--  id_target INTEGER REFERENCES TARGET_GOSPROGRAM_VO(id),
--CONSTRAINT INDICATIONS_RF_TARGET_PK
--  PRIMARY KEY (id_ind_rf, id_target));
