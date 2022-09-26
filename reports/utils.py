import requests
from .models import Vehicle, \
    Osago, \
    VehiclePeriods, \
    Wanted, \
    Restrict, \
    Dtp, \
    DiagnosticsActive, \
    DiagnosticsExpired, \
    Pledges, \
    Reviews, \
    Taxi, \
    CustomsClearance, \
    RNISRegister, \
    VinDecode, \
    Image
from profiles.models import Profiles

def get_restrict_car_info(request, type, number):
    if type == 'VIN':
        type = 'vin'
    else:
        type = 'regNumber'

    TOKEN = 'ae3b2fa0e7d3f7dec39b99cb59421e81'

    result = {}

    if type == 'regNumber':
        rsa_response = requests.get(f'https://api-cloud.ru/api/rsa.php?'
                                    f'type=osago'
                                    f'&{type}={number}'
                                    f'&token={TOKEN}')
        rsa_data = rsa_response.json()
        try:
            result['message'] = rsa_data['message']
            return result
        except:
            vin = rsa_data['rez'][0]['vin']
            gibdd_response = requests.get('https://api-cloud.ru/api/gibdd.php?'
                                          'type=gibdd'
                                          f'&vin={vin}'
                                          f'&token={TOKEN}')
            gibdd_data = gibdd_response.json()
            result['model'] = gibdd_data['vehicle']['model']
            result['color'] = gibdd_data['vehicle']['color']
            result['year'] = gibdd_data['vehicle']['year']

    elif type == 'vin':
        vin = number
        gibdd_response = requests.get('https://api-cloud.ru/api/gibdd.php?'
                                      'type=gibdd'
                                      f'&vin={vin}'
                                      f'&token={TOKEN}')
        gibdd_data = gibdd_response.json()
        try:
            result['message'] = gibdd_data['message']
            return result
        except:
            result['model'] = gibdd_data['vehicle']['model']
            result['color'] = gibdd_data['vehicle']['color']
            result['year'] = gibdd_data['vehicle']['year']

    return result

def create_car_info(request, type, number):
    if type == 'VIN':
        type = 'vin'
    else:
        type = 'regNumber'

    TOKEN = 'ae3b2fa0e7d3f7dec39b99cb59421e81'

    errors = {}
    messages = {}

    rsa_response = requests.get(f'https://api-cloud.ru/api/rsa.php?'
                                f'type=osago'
                                f'&{type}={number}'
                                f'&token={TOKEN}')
    rsa_data = rsa_response.json()
    try:
        messages['osago'] = rsa_data['massage']
        return messages, errors
    except:
        pass

    if type == 'vin':
        vin = number
        regnum = rsa_data['rez'][0]['regnum']
    else:
        regnum = number
        vin = rsa_data['rez'][0]['vin']

    gibdd_response = requests.get('https://api-cloud.ru/api/gibdd.php?'
                                  'type=gibdd'
                                  f'&vin={vin}'
                                  f'&token={TOKEN}')

    gibdd_data = gibdd_response.json()
    try:
        messages['main_info'] = gibdd_data['massage']
        return messages, errors
    except:
        pass

    vehicle = Vehicle(
        profile=Profiles.object.get(email=request.user),

        vin=vin,
        gos_number=regnum,
        body_number=gibdd_data['vehicle']['bodyNumber'],
        engine_number=gibdd_data['vehicle']['engineNumber'],
        model=gibdd_data['vehicle']['model'],
        color=gibdd_data['vehicle']['color'],
        year=gibdd_data['vehicle']['year'],
        engine_volume=gibdd_data['vehicle']['engineVolume'],
        power_hp=gibdd_data['vehicle']['powerHp'],
        power_kwt=gibdd_data['vehicle']['powerKwt'],
        category=gibdd_data['vehicle']['category']
    )
    vehicle.save()

    try:
        osago = Osago(
            vehicle=vehicle,

            seria=rsa_data['rez'][0]['seria'],
            number=rsa_data['rez'][0]['nomer'],
            organization=rsa_data['rez'][0]['orgosago'],
            status=rsa_data['rez'][0]['status'],
            term=rsa_data['rez'][0]['term'],
            region=rsa_data['rez'][0]['region'],
            restrictions=rsa_data['rez'][0]['ogran'],
            action=rsa_data['rez'][0]['sledToRegorTo'],
            usage_purposes=rsa_data['rez'][0]['cel'],
            insured=rsa_data['rez'][0]['insured'],
            owner=rsa_data['rez'][0]['owner'],
            date_actual=rsa_data['rez'][0]['dateactual']
        )
        osago.save()
    except Exception as e:
        errors['osago'] = e

    for owner in gibdd_data['ownershipPeriod']:
        try:
            periods = VehiclePeriods(
                vehicle=vehicle,

                reason=owner['lastOperationInfo'],
                owner=owner['simplePersonTypeInfo'],
                date_from=owner['from'],
                to=owner['to'],
                period=owner['period']
            )
            periods.save()
        except Exception as e:
            errors['periods'] = e

    wanted_response = requests.get('https://api-cloud.ru/api/gibdd.php?'
                                   'type=wanted'
                                   f'&vin={vin}'
                                   f'&token={TOKEN}')
    wanted_data = wanted_response.json()

    try:
        messages['wanted'] = wanted_data['message']
    except:
        for wanted in wanted_data['records']:
            record = Wanted(
                vehicle=vehicle,
                region=wanted['w_reg_inic'],
                model=wanted['w_model'],
                date=wanted['w_data_pu'],
                vin=wanted['w_vin'],
                date_car=wanted['w_god_vyp']

            )
            record.save()

    restrict_response = requests.get('https://api-cloud.ru/api/gibdd.php?'
                                     'type=restrict'
                                     f'&vin={vin}'
                                     f'&token={TOKEN}')
    restrict_data = restrict_response.json()

    try:
        messages['restrict'] = restrict_data['message']
    except:
        for restrict in restrict_data['records']:
            restrict_record = Restrict(
                vehicle=vehicle,

                region=restrict['regname'],
                basis_restrict=restrict['osnOgr'],
                date_from=restrict['dateog'],
                date_to=restrict['dateadd'],
                restrict=restrict['ogrkodinfo'],
                who_imposed=restrict['divtypeinfo']
            )
            restrict_record.save()

    dtp_response = requests.get('https://api-cloud.ru/api/gibdd.php?'
                                'type=dtp'
                                f'&vin={vin}'
                                f'&token={TOKEN}')
    dtp_data = dtp_response.json()

    try:
        messages['dtp'] = dtp_data['message']
    except:
        for dtp in dtp_data['records']:
            dtp_record = Dtp(
                vehicle=vehicle,

                date=dtp['AccidentDateTime'],
                damage=dtp['VehicleDamageState'],
                type=dtp['AccidentType'],
                damage_description=dtp['DamageDestription'],
                place=dtp['AccidentPlace']
            )
            dtp_record.save()

    diagnostic_response = requests.get('https://api-cloud.ru/api/gibdd.php?'
                                       f'vin={vin}'
                                       '&type=eaisto'
                                       f'&token={TOKEN}')
    diagnostic_data = diagnostic_response.json()

    try:
        messages['diagnostic'] = diagnostic_data['message']
    except:
        diagnostic_active = DiagnosticsActive(
            vehicle=vehicle,

            from_date=diagnostic_data['records'][0]['dcDate'],
            expire_date=diagnostic_data['records'][0]['dcExpirationDate'],
            value=diagnostic_data['records'][0]['odometerValue'],
            dc_number=diagnostic_data['records'][0]['dcNumber'],
            point_address=diagnostic_data['records'][0]['pointAddress']
        )
        diagnostic_active.save()
        for prvs_docs in diagnostic_data['records'][0]['previousDcs']:
            try:
                diagnostic_expire = DiagnosticsExpired(
                    vehicle=vehicle,

                    from_date=prvs_docs['dcDate'],
                    expire_date=prvs_docs['dcExpirationDate'],
                    value=prvs_docs['odometerValue'],
                    dc_number=prvs_docs['dcNumber'],
                )
                diagnostic_expire.save()
            except Exception as e:
                errors['prvs_docs'] = e

    pledges_response = requests.get('https://api-cloud.ru/api/zalog.php?'
                                    'type=notary'
                                    f'&vin={vin}'
                                    f'&token={TOKEN}')
    pledges_data = pledges_response.json()

    try:
        messages['pledges'] = pledges_data['message']
    except:
        for pledge in pledges_data['rez']:
            pledge_record = Pledges(
                vehicle=vehicle,

                record_date=pledge['regDate'],
                pledge_give=pledge['pledgors'][0]['name'],
                pledge_give_birthday=pledge['pledgors'][0]['birthday'],
                pledge_get=pledge['pledgees'][0]['name']

            )
            pledge_record.save()

    reviews_response = requests.get('https://api-cloud.ru/api/gost.php?'
                                    'type=vin'
                                    f'&vin={vin}'
                                    f'&token={TOKEN}')
    reviews_data = reviews_response.json()

    try:
        messages['reviews'] = reviews_data['message']
    except:
        review = Reviews(
            vehicle=vehicle,

            date=reviews_data['date'],
            organization=reviews_data['organizator'],
            reason=reviews_data['reasons'],
            recommendation=reviews_data['recommendation']
        )
        review.save()

    taxi_response = requests.get('https://api-cloud.ru/api/taxi/v2/taxi.php?'
                                 'type=regnum'
                                 f'&regnum={regnum}'
                                 f'&token={TOKEN}')
    taxi_data = taxi_response.json()

    try:
        messages['taxi'] = taxi_data['message']
    except:
        taxi = Taxi(
            vehicle=vehicle,

            number=taxi_data[0]['permitNumber'],
            organization=taxi_data[0]['perevoz'],
            date_from=taxi_data[0]['dateFrom'],
            date_to=taxi_data[0]['dateTo'],
            status=taxi_data[0]['status'],
            region=taxi_data[0]['regionName']
        )
        taxi.save()

    customs_response = requests.get('https://api-cloud.ru/api/fts.php?'
                                    'type=auto'
                                    f'&vin={vin}'
                                    f'&token={TOKEN}')
    customs_data = customs_response.json()

    try:
        messages['customs'] = customs_data['message']
    except:
        customs = CustomsClearance(
            vehicle=vehicle,

            model=customs_data[0]['model']['value'],
            date=customs_data[0]['date']['value']
        )
        customs.save()

    rnis_response = requests.get('https://api-cloud.ru/api/transportMos.php?'
                                 'type=rnis'
                                 f'&regNum={regnum}'
                                 f'&token={TOKEN}')
    rnis_data = rnis_response.json()

    try:
        messages['rnis'] = rnis_data['message']
    except:
        rnis = RNISRegister(
            vehicle=vehicle,

            vehicle_exists=rsa_data['vehicleExists'],
            last_mark=rsa_data['lastMark'],
            is_online=rsa_data['isOnline']
        )
        rnis.save()

    vin_decode_response = requests.get('https://api-cloud.ru/api/vindecoder.php?'
                                       'type=vin'
                                       f'&vin={vin}'
                                       f'&token={TOKEN}')
    vin_decode_data = vin_decode_response.json()

    try:
        messages['vin_decode'] = vin_decode_data['errormsg']
    except:
        vin_decode = VinDecode(
            vehicle=vehicle,

            wmi=vin_decode_data['WMI']['value'],
            vis=vin_decode_data['VIS identifier']['value'],
            vds=vin_decode_data['VDS']['value'],
            year_identifier=vin_decode_data['Year_identifier']['value'],
            serial_number=vin_decode_data['Serial_number']['value'],
            vin_type=vin_decode_data['VIN_type']['value'],
            body_type=vin_decode_data['Body']['value'],
            engine_type=vin_decode_data['Engine']['value'],
            fuel_type=vin_decode_data['Fuel']['value'],
            transmission_type=vin_decode_data['Transmission']['value'],
            car_class=vin_decode_data['classCar']['value'],
            car_type=vin_decode_data['typeCar']['value'],
            body_diff=vin_decode_data['Body_type']['value'],
            number_doors=vin_decode_data['Number_doors']['value'],
            number_seats=vin_decode_data['Number_seats']['value'],
            engine_valves=vin_decode_data['Engine_valves']['value'],
            cylinders=vin_decode_data['cylinders']['value'],
            transmission=vin_decode_data['gearbox']['value']
        )
        vin_decode.save()

    photo_response = requests.get('https://api-cloud.ru/api/autophoto.php?'
                                  'type=regnum'
                                  f'&regNum={regnum}'
                                  f'&token={TOKEN}')
    photo_data = photo_response.json()
    try:
        messages['photo'] = photo_data['message']
    except:
        for url in photo_data['records']:
            pic = Image(
                vehicle=vehicle,

                img=url['bigPhoto']
                )
            pic.save()
    return messages, errors, vehicle
