import Col from "react-bootstrap/Col";
import Skeleton from "react-loading-skeleton";
const ItemSkeleton = () => {
    return (
        <Col>
            <Skeleton width="100%" height="50vh" />
        </Col>
    );
};

export default ItemSkeleton;
