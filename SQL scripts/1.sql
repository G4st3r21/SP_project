SELECT A6.events as Мероприятие, '2016' as Год
FROM ALL_EVENTS2016 A6
WHERE A6.code IN
      (SELECT CODE_EVENTS
       FROM EVENTS_RESPONSE_FIO2016
       WHERE ID_FIO IN
             (SELECT ID
              FROM RESPONSE_FIO2016
              WHERE FIO LIKE '%Салогубов%'))
UNION ALL
SELECT A7.events as Мероприятие, '2017' as Год
FROM ALL_EVENTS2016 A7
WHERE A7.code IN
      (SELECT CODE_EVENTS
       FROM EVENTS_RESPONSE_FIO2017
       WHERE ID_FIO IN
             (SELECT ID
              FROM RESPONSE_FIO2017
              WHERE FIO LIKE '%Салогубов%'))
UNION ALL
SELECT A8.events as Мероприятие, '2018' as Год
FROM ALL_EVENTS2018 A8
WHERE A8.code IN
      (SELECT CODE_EVENTS
       FROM EVENTS_RESPONSE_FIO2018
       WHERE ID_FIO IN
             (SELECT ID
              FROM RESPONSE_FIO2018
              WHERE FIO LIKE '%Салогубов%'))
UNION ALL
SELECT A9.events as Мероприятие, '2019' as Год
FROM ALL_EVENTS2019 A9
WHERE A9.code IN
      (SELECT CODE_EVENTS
       FROM EVENTS_RESPONSE_FIO2019
       WHERE ID_FIO IN
             (SELECT ID
              FROM RESPONSE_FIO2019
              WHERE FIO LIKE '%Салогубов%'))
UNION ALL
SELECT A10.events as Мероприятие, '2020' as Год
FROM ALL_EVENTS2020 A10
WHERE A10.code IN
      (SELECT CODE_EVENTS
       FROM EVENTS_RESPONSE_FIO2020
       WHERE ID_FIO IN
             (SELECT ID
              FROM RESPONSE_FIO2020
              WHERE FIO LIKE '%Салогубов%'));
