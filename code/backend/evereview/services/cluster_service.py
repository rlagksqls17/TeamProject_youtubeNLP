from evereview.models.cluster import db, Cluster
from evereview.models.code import Code


def get_cluster(cluster_id):
    result = (
        Cluster.query.join(Code, Cluster.code == Code.id)
        .add_columns(Code.description)
        .filter_by(Cluster.id == cluster_id)
        .one_or_none()
    )

    return result


def get_clusters(analysis_id):
    result = (
        Cluster.query.join(Code, Cluster.code == Code.id)
        .add_columns(
            Cluster.id,
            Cluster.code,
            Cluster.top_comment,
            Cluster.count,
            Cluster.like_count,
            Code.description,
        )
        .filter(Cluster.analysis_id == analysis_id)
        .all()
    )

    return result
