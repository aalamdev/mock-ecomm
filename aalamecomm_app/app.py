import json
import os
import webob.exc

from aalam_common.config import cfg
from aalam_common.redisdb import redis_conn
from aalam_common import wsgi
from aalam_common import sqa as zsqa
from aalam_common import CALLBACK_ROUTES, STATE_VALIDATION


class EcommAppHandler(wsgi.BaseHandler):
    def __init__(self, mapper):
        super(EcommAppHandler, self).__init__(mapper)
        
    def create_order(self, request):
        return {"id": 1}

    def update_order(self, request, order_id):
        if 'status' not in request.params:
            raise webob.exc.HTTPBadRequest(
              explanation="'status' parameter is mandatory")
        if request.params['status'] not in ['New', 'Cancelled', 'Return-Initiated',
                                            'Return-Shipped', 'Refunded']:
            raise webob.exc.HTTPBadRequest(
                explanation="Invalid status value")
 
    def getorder_details(self, request, order_id):
        with open(os.path.join(cfg.CONF.statics_dir, 'getorderdetails.json'), 'r') as f:
            getorderdetails_dict = json.load(f)
            return getorderdetails_dict

    def get_orders(self, request):
        with open(os.path.join(cfg.CONF.statics_dir, 'getorders.json'), 'r') as f:
            getorders_dict = json.load(f)
            return getorders_dict

    def getall_settings(self, request):
        with open(os.path.join(cfg.CONF.statics_dir,
                               'getallsettings.json'), 'r') as f:
            getallsettings_dict = json.load(f)
            return getallsettings_dict

    def getitem_groups(self, request, item_id):
        with open(os.path.join(cfg.CONF.statics_dir, 'getitemgroups.json'), 'r') as f:
            getitemgroups_dict = json.load(f)
            return getitemgroups_dict

    def getitem_props(self, request):
        with open(os.path.join(cfg.CONF.statics_dir, 'getitemprops.json'), 'r') as f:
            getitemprops_dict = json.load(f)
            return getitemprops_dict

    def prune_order(self, request, order_id):
        with open(os.path.join(cfg.CONF.statics_dir, 'pruneorder.json'), 'r') as f:
            pruneorder_dict = json.load(f)
            return pruneorder_dict

    def items_order(self, request, order_id, items=[]):
    	return

    def _redisify_item_key(self, name):
        return "aalamecomm-%s" % name

    def addcart_item(self, request, item_id):
      redis_conn.hset(self._redisify_item_key('cart'), item_id, 1)

    def update_item(self, request, item_id):
      if 'quantity' not in request.params:
          raise webob.exc.HTTPBadRequest(explanation="Invalid usage")
      
      k = self._redisify_item_key('cart')
      redis_conn.hset(k, item_id, request.params['quantity'])
      
    def delete_item(self, request, item_id):
      k = self._redisify_item_key('cart')
      redis_conn.hdel(k, item_id)

    def empty_cart(self, request):
      redis_conn.delete(self._redisify_item_key('cart'))

    def get_cart(self, request):
      ret = redis_conn.hgetall(self._redisify_item_key('cart'))
      return [{'item_id': int(k), 'quantity': float(v)} for k, v in ret.iteritems()]

    def check_coupons(self, request, coupon_code):
        with open(os.path.join(cfg.CONF.statics_dir, 'checkcoupons.json'), 'r') as f:
            checkcoupons_dict = json.load(f)
            return checkcoupons_dict

    def biz_settings(self, request):
        with open(os.path.join(cfg.CONF.statics_dir, 'bizsettings.json'), 'r') as f:
            bizsettings_dict = json.load(f)
            return bizsettings_dict

    def contact_details(self, request):
        with open(os.path.join(cfg.CONF.statics_dir, 'contactdetails.json'), 'r') as f:
            contactdetails_dict = json.load(f)
            return contactdetails_dict
       
    def display_logo(self, request):
        request.static_file = {"resource": "logo.png",
                               "path": os.path.join(cfg.CONF.statics_dir,
                                                    "logo.png")}

    def style(self, request):
        request.static_file = {"resource": "styles.css",
                               "path": os.path.join(cfg.CONF.statics_dir,
                                                    "styles.css")}

    def preorder(self, request):
    	with open(os.path.join(cfg.CONF.statics_dir, 'settings.json'), 'r') as f:
    	    settings_dict = json.load(f)
    	    return settings_dict


def routes_cb(mapper):
    with mapper.submapper(handler=EcommAppHandler(mapper)) as m:

        m.connect("/aalam/ecomm/orders",
                  action="create_order",
                  conditions={"method": ['PUT']})

        m.connect("/aalam/ecomm/order/{order_id}",
                  action="update_order",
                  conditions={"method": ['POST']})

        m.connect("/aalam/ecomm/order/{order_id}",
                  action="getorder_details",
                  conditions={"method": ['GET']})

        m.connect("/aalam/ecomm/orders",
                  action="get_orders",
                  conditions={"method": ['GET']})

        m.connect("/aalam/ecomm/setting/_all_",
                  action="getall_settings",
                  conditions={"method": ['GET']})

        m.connect("/aalam/ecomm/setting/item_group/item/{item_id}",
                  action="getitem_groups",
                  conditions={"method": ['GET']})

        m.connect("/aalam/ecomm/setting/item_groups/props",
                  action="getitem_props",
                  conditions={"method": ['GET']})

        m.connect("/aalam/ecomm/order/{order_id}/prune",
                  action="prune_order",
                  conditions={"method": ['POST']})

        m.connect("/aalam/ecomm/order/{order_id}/items",
                  action="items_order",
                  conditions={"method": ['PUT']})

        m.connect("/aalam/ecomm/cart",
                  action="addcart_item",
                  conditions={"method": ['PUT']})

        m.connect("/aalam/ecomm/cart/item/{item_id}",
                  action="update_item",
                  conditions={"method": ['POST']})

        m.connect("/aalam/ecomm/cart/item/{item_id}",
                  action="delete_item",
                  conditions={"method": ['DELETE']})

        m.connect("/aalam/ecomm/cart",
                  action="empty_cart",
                  conditions={"method": ['DELETE']})

        m.connect("/aalam/ecomm/cart",
                  action="get_cart",
                  conditions={"method": ['GET']})

        m.connect("/aalam/ecomm/cart/coupon/{coupon_code}",
                  action="check_coupons",
                  conditions={"method": ['POST']})

        m.connect("/aalam/ecomm/r/j/biz-settings",
                  action="biz_settings",
                  conditions={"method": ['GET']})

        m.connect("/aalam/ecomm/contact",
                  action="contact_details",
                  conditions={"method": ['GET']})

        m.connect("/aalam/ecomm/i/brand.img",
                  action="display_logo",
                  conditions={"method": ['GET']})

        m.connect("/aalam/ecomm/r/css/styles.css",
                  action="style",
                  conditions={"method": ['GET']})

        m.connect("/aalam/ecomm/setting/preorder",
       			  action="preorder",
        		  conditions={"method": ['GET']})


def entry(state):
    if state != STATE_VALIDATION:
        pass

    return {CALLBACK_ROUTES: routes_cb}
