from evereview.models.analysis import db, Analysis


def get_analysis(analysis_id):
    result = Analysis.query.filter_by(id=analysis_id).one_or_none()

    return result


def get_analysises(user_id):
    analysises = Analysis.query.filter_by(id=user_id).all()

    result = []
    for analysis in analysises:
        result.append(analysis.to_dict())

    return result
