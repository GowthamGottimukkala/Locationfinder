import React,{Component} from 'react';
import GoogleMapReact from 'google-map-react';

class Map extends Component{
    render(){
        return(
            <div style={{height:'1000px',width:'1000px'}}>
                <GoogleMapReact bootstrapURLKeys={{ key:'AIzaSyCLXUeNBnr-U_526lUfTfpPFg6Y6h9ogg4' }} defaultCenter={{lat:this.props.lat,lng:this.props.lng}} defaultZoom={14} />
            </div>
        );
    }
}

export default Map;