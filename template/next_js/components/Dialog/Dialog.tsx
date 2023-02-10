import React, {useEffect} from 'react';
import Dialog from '@mui/material/Dialog';


/**
 * DialogProps
 */
interface __dialog_id__Prop {
    isOpen: boolean;
    setIsOpen: React.Dispatch<React.SetStateAction<boolean>>;
}


/**
 * __summary__
 *　TODO: This class is auto generated by yaml_to_view program.
 * __comment__
 *
 * version: __version__
 * @constructor
 */
const __dialog_id__ = (prop: __dialog_id__Prop) => {


    // Close Dialog
    const handleClose = () => {
        prop.setIsOpen(false);
    };


    /**
     * Use effect: ダイアログ初期化処理
     */
    useEffect(() => {

    }, [prop]);


    /**
     * Render
     */
    return (
        <Dialog
            open={prop.isOpen}
            onClose={handleClose}
            >

        </Dialog>
    );
}

export default __dialog_id__;
